from battleships.models.game import Game
from battleships.models.player import Player
from battleships.utils.message_utils import parse_message, push_message
from battleships.utils.test_data_set import TestDataSet
from battleships.models.serializers import GameSerializer
from battleships.models.game import FireMessage, InvalidMessage, MoveMessage, IdleMessage, Message, OutputMessage, MessageType
from battleships.models.game_player import GamePlayer
from django.http import HttpResponse, HttpRequest
from django.core import serializers
from .forms import NewGameForm
from django.shortcuts import render
import json
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from battleships.forms import SignUpForm
import jsonpickle
import logging
from django.views.decorators.csrf import csrf_exempt
from channels import Group

logger = logging.getLogger("battleships.views.py")


# sign up
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.player.nick = form.cleaned_data.get('nickname')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=user.username, password=raw_password, email=email)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# creates score ranking
class PlayerListView(ListView):
    model = Player
    paginate_by = 100
    queryset = Player.objects.order_by('-score')


# renders game template
def open_game(request, game_id, game_name):
    if not request.user.is_authenticated:
        return HttpResponse(status=403)
    return render(request, 'game.html')


# creates game, returns link to it
def new_game(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=403)
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            game = Game(boardSize=40, max_players=2, name=request.POST['name'])
            game.save()
            game_url = 'http://' + get_current_site(request).domain + '/game/' + str(game.id) + '/' + game.name.replace(" ", "_")
            response = {
                'url': game_url,
                'game_name': game.name
            }
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            return HttpResponse(json.dumps(form.errors))
    else:
        return render(request, 'new_game.html', {'form': NewGameForm})


# adds new player to game
def add_player(request, game_id):
    if not request.user.is_authenticated:
        return HttpResponse(status=403)
    game = Game.objects.get(id=game_id)

    if game.is_max_players():  # when board is full not anymore players can join it
        return HttpResponse(json.dumps("No more players can join!"),  status=403)
    player = Player.objects.get(user_id=request.user.id)
    game_player = GamePlayer(player_id=player.id, game_id=game.id, game_nick=player.nick)
    if game.gameplayer_set.count() == 0:
        game_player.inControl = True
    game_player.index = game.gameplayer_set.count() + 1
    game_player.save()
    game_player.attach_ships(TestDataSet.get_ships_set(game.get_players_count(), game.boardSize))
    init_session(request, game_id, game.get_player_id(request.user.id))

    output_message = OutputMessage("New player has joined!", MessageType.PLAYER_ADDITION_SUCCESS, request.user.id)
    push_message(game_id, game_player.id, game_player.game_nick, output_message)

    if game.is_max_players():  # after player addition board is full so start the game
        output_message = OutputMessage("The game has begun", MessageType.GAME_BEGIN)
        push_message(game_id, game_player.id, game_player.game_nick, output_message)
    return HttpResponse(json.dumps("Player successfully added!"), status=200)


# parses message received from client and invokes proper game method then pushes return message via web socket
# <  simple http request  >
#def play(request, game_id, game_name, raw_message):
@csrf_exempt
def play(request, game_id, game_name):
    if not request.user.is_authenticated:
        return HttpResponse(status=403)

    if request.method == 'POST':
        raw_message = json.loads(request.body.decode('utf-8'))['message']
        game = Game.objects.get(id=game_id)
        game_player = game.get_player(request.user.id)
        if game_player.lost:
            return HttpResponse(status=403)
        game_player_id = game_player.id
        message = parse_message(raw_message)
        push_message(game_id, game_player_id, game_player.game_nick, OutputMessage(message.text, MessageType.COMMAND))

        if game.is_game_finished():
            push_message(game_id, game_player_id, game_player.game_nick, OutputMessage("Cannot perform action, game already finished!", MessageType.GAME_FINISHED))
            return HttpResponse(status=403)

        if game_player.lost:
            push_message(game_id, game_player_id, game_player.game_nick,OutputMessage("Cannot perform action, you already lost the game!", MessageType.GAME_FINISHED))
            return HttpResponse(status=403)

        if not game.all_players_ready():
            push_message(game_id, game_player_id, game_player.game_nick, OutputMessage("Cannot perform action, waiting for players to join the game...", MessageType.GAME_NOT_STARTED))
            return HttpResponse(status=403)

        if isinstance(message, FireMessage):
            if game.is_player_turn(game_player_id):
                output_message = game.fire_ship(game_player_id, message.attacker, message.defender)
                push_message(game_id, game_player_id, game_player.game_nick, output_message)
                if not output_message.message_type == MessageType.FIRE_FAILURE:
                    output_message = game.play()
                    game.save()
                    push_message(game_id, game_player_id, game_player.game_nick, output_message)
            else:
                push_message(game_id, game_player_id, game_player.game_nick, OutputMessage("Cannot perform action, it is not your turn!", MessageType.WRONG_ROUND))
                return HttpResponse(status=403)
        elif isinstance(message, MoveMessage):
            if game.is_player_turn(game_player_id):
                output_message = game.move_ship(game_player_id, message.mover, message.move_type)
                push_message(game_id, game_player_id, game_player.game_nick, output_message)
                if not output_message.message_type == MessageType.MOVE_FAILURE:
                    output_message = game.play()
                    game.save()
                    push_message(game_id, game_player_id, game_player.game_nick, output_message)
            else:
                push_message(game_id, game_player_id, game_player.game_nick, OutputMessage("Cannot perform action, it is not your turn!", MessageType.WRONG_ROUND))
                return HttpResponse(status=403)
        elif isinstance(message, IdleMessage):
            if game.is_player_turn(game_player_id):
                output_message = game.play()
                push_message(game_id, game_player_id, game_player.game_nick, output_message)
            else:
                push_message(game_id, game_player_id, game_player.game_nick, OutputMessage("Cannot perform action, it is not your turn!", MessageType.WRONG_ROUND))
                return HttpResponse(status=403)
        elif isinstance(message, InvalidMessage):
            #pass
            push_message(game_id, game_player_id, game_player.game_nick, OutputMessage("Bad format!", MessageType.BAD_FORMAT, request.user.id))
        elif isinstance(message, Message):
            output_message = OutputMessage(message.get_text(), MessageType.MESSAGE)
            push_message(game_id, game_player_id, game_player.game_nick, output_message)
        return HttpResponse(request.user.id, status=200)
    else:
        return HttpResponse(status=403)


# method checks if user who opened the game is a game player if not then enables joining
# returns code 200 when player can join game/already joined game earlier, returns code 403 when game is full
def join_game(request, game_id, game_name):
    if not request.user.is_authenticated:
        return HttpResponse(status=403)
    try:
        game = Game.objects.get(id=game_id)
        if game.is_player(request.user.id):
            init_session(request, game_id, game.get_player_id(request.user.id))
            return HttpResponse(json.dumps("Loading game!"), status=200)
        else:
            return add_player(request, game_id)  # try to add player to the game
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps("An unexpected error occurred"),  status=404)


# todo should return only info needed by one player,
# todo maybe only list with player ships(with associated visibility coordinates list) + list of visible enemy ships
# temporary solution: returns all players game data < in json format >
def refresh_ui(request, game_id, game_name):
    if not request.user.is_authenticated:
        return HttpResponse(status=403)
    # should return all game_players, basing on the returned data the client side will fill the board and color it ( and assign name for each ship )
    game = Game.objects.get(id=game_id)
    serializer = GameSerializer(game)
    #return HttpResponse(json.dumps(serializer), status=404)
    return JsonResponse(serializer.data, safe=False)


def init_session(request, game_id, game_player_id):
    request.session['game_id'] = game_id
    request.session['game_player_id'] = game_player_id



# HOW THIS WORKS?
# client side listens to web socket events<messages>, every received event should trigger client ui refresh
# to update clients ui refresh_ui method should be requested
# Besides, client side can also perform actions in game.
# to do that client side needs to invoke process_message method by sending to it appropriate commands as a text message
# after parsing process completes, proper game action is being invoked
# each game action result<or parsing error> is passed to all clients as a web socket event<message>
