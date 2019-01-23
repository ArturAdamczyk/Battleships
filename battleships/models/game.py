from django.db import models
from battleships.models.ship import Move
import json
import random

MISS_CHANCE_VALUE = 3
MISS_VALUE = 1

class FireResult:
    HIT = "hit"
    FIRE = "fire"
    PASS = "pass"
    MESSAGE = "message"
    INVALID = "invalid"


class Commands:
    MOVE = "move"
    FIRE = "fire"
    PASS = "pass"
    MESSAGE = "msg"
    INVALID = "invalid"


class Message:
    command = Commands.MESSAGE
    user_id = ""
    text = ""
    user_name = ""

    def __init__(self, text):
        self.text = text

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_text(self):
        return self.text


class FireMessage(Message):
    command = Commands.FIRE
    attacker = ""
    defender = ""

    def __init__(self, text):
        Message.__init__(self, text)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_text(self):
        super(FireMessage, self).get_text()


class MoveMessage(Message):
    command = Commands.MOVE
    mover = ""
    move_type = ""

    def __init__(self, text):
        Message.__init__(self, text)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_text(self):
        super(MoveMessage, self).get_text()


class IdleMessage(Message):
    command = Commands.PASS

    def __init__(self, text):
        Message.__init__(self, text)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_text(self):
        super(IdleMessage, self).get_text()


class InvalidMessage(Message):
    command = Commands.INVALID

    def __init__(self, text):
        Message.__init__(self, text)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_text(self):
        super(InvalidMessage, self).get_text()


class MessageType:
    MOVE_SUCCESS = "MOVE SUCCESS"
    MOVE_FAILURE = "MOVE FAILURE"
    FIRE_SUCCESS = "FIRE SUCCESS"
    FIRE_MISS = "FIRE MISS"
    FIRE_FAILURE = "FIRE FAILURE"
    GAME_END = "GAME END"
    GAME_BEGIN = "GAME BEGIN"
    GAME_FINISHED = "GAME FINISHED"
    GAME_NOT_STARTED = "GAME NOT STARTED"
    NEW_PLAYER = "NEW PLAYER"
    NEXT_ROUND = "NEXT ROUND"
    WRONG_ROUND = "WRONG ROUND"
    PLAYER_ADDITION_SUCCESS = "PLAYER ADDITION SUCCESS"
    PLAYER_ADDITION_FAILURE = "PLAYER ADDITION FAILURE"
    PASS_ROUND = "PASS ROUND"
    MESSAGE = "MESSAGE"
    BAD_FORMAT = "BAD FORMAT"
    COMMAND = "COMMAND"


class OutputMessage:
    message = ""
    message_type = ""
    receiver = ""

    def __init__(self, message, message_type, receiver=""):
        self.message = message
        self.message_type = message_type
        self.receiver = receiver

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


# create GameMessage with result string from move and fire funcs
class Game(models.Model):
    MAX_DAMAGE = 10

    winner = models.OneToOneField('GamePlayer', on_delete='cascade', default=None, blank=True, null=True, related_name="winner")
    name = models.CharField(max_length=200, default='')
    boardSize = models.IntegerField(default=20)
    finished = models.BooleanField(default=False)
    max_players = models.IntegerField(default=4)

    def is_player(self, user_id)-> bool:
        if self.gameplayer_set.all().exists():
            for player in self.gameplayer_set.all():
                if player.player_id == user_id:
                    return True
        return False

    # TO SIMPLIFY ASSUMING THAT GAME_PLAYER.PLAYER == PLAYER.ID == USER.ID;  IN FACT PLAYER AND USER DEPEND ON EACH
    def get_player_id(self, user_id):
        for game_player in self.gameplayer_set.all():
            if game_player.player == user_id:
                return game_player.player

    def get_game_player(self, user_id):
        for game_player in self.gameplayer_set.all():
            if game_player.player == user_id:
                return game_player

    def get_player(self, player_id):
        return self.gameplayer_set.get(player=player_id)

    def add_player(self, user_id)-> OutputMessage:
        if self.gameplayer_set.count() < self.max_players:
            #GamePlayer(player=user_id, game=self.id).save()  # todo is it enough?
            #self.gameplayer_set.add(GamePlayer(player=user_id, game=self.id))
            return OutputMessage("Player added successfully", MessageType.PLAYER_ADDITION_SUCCESS, user_id)
        else:
            return OutputMessage("Game is full!", MessageType.PLAYER_ADDITION_FAILURE, user_id)

    def play(self)-> OutputMessage:
        self.refresh_game_status()
        if not self.finished:
            return self.next_round()
        else:
            return OutputMessage("Game finished, player " + self.winner.game_nick + " won!", MessageType.GAME_END, self.winner.id)

    def refresh_game_status(self):
        lost_players = 0
        winner = None
        for player in self.gameplayer_set.all():
            if player.lost:
                lost_players += 1
            else:
                winner = player
        if self.max_players - lost_players == 1:
            self.winner = winner
            self.finished = True
            self.winner.increase_score()
            self.winner.save()

    def next_round(self)-> OutputMessage:
        counter = 0
        game_players = list(self.gameplayer_set.all())

        for player in game_players:
            if player.inControl:
                if self.gameplayer_set.count() == counter + 1:
                    player_in_control = game_players[0]
                else:
                    player_in_control = game_players[counter + 1]
                player_in_control.inControl = True
                old_player_in_control = game_players[counter]
                old_player_in_control.inControl = False
                if self.gameplayer_set.count() == counter + 1:
                    player_in_control.save()
                    old_player_in_control.save()
                else:
                    old_player_in_control.save()
                    player_in_control.save()
                return OutputMessage(
                    "Next round: Player " +
                    player_in_control.game_nick +
                    " in control",
                    MessageType.NEXT_ROUND,
                    player_in_control.id)
            counter += 1

    def get_player_in_control(self):
        for player in self.gameplayer_set.all():
            if player.inControl:
                return player

    def is_player_turn(self, player_id):
        return player_id == self.get_player_in_control().id

    def move_ship(self, user, ship_name, direction)-> OutputMessage:
        ship = self.gameplayer_set.get(id=user).find_ship(ship_name)
        if ship is None:
            return OutputMessage("Not found", MessageType.MOVE_FAILURE)
        if ship.is_sunk():
            return OutputMessage("Not found", MessageType.MOVE_FAILURE)
        # check if no other ship blocks movement or if move does not exceed game board
        for game_player in self.gameplayer_set.all():
            if not game_player.is_move_possible(ship, direction, self.boardSize):
                return OutputMessage("Move not possible", MessageType.MOVE_FAILURE)
        ship.move(direction)
        return OutputMessage("Ship moved!", MessageType.MOVE_SUCCESS)

    def fire_ship(self, attacking_user, attacking_ship_name, defending_ship_name)-> OutputMessage:
        defending_ship = None
        for game_player in self.gameplayer_set.all():
            if defending_ship is None:
                defending_ship = game_player.find_ship(defending_ship_name)
            else:
                break
        game_player = self.gameplayer_set.get(id=attacking_user)
        attacking_ship = game_player.find_ship(attacking_ship_name)
        if defending_ship is None or attacking_ship is None:
            return OutputMessage("Not found", MessageType.FIRE_FAILURE)
        if defending_ship.is_sunk() or attacking_ship.is_sunk():
            return OutputMessage("Not found", MessageType.FIRE_FAILURE)

        # todo uncomment and add visibility feature
        attacking_ship_visible_positions = attacking_ship.get_visibility_range_coordinates()
        # if at least one part[position] of defending ship is visible by the attacking ship -> than fire
        #for range_position in attacking_ship_visible_positions:
        #    for defending_ship_position in defending_ship.objects:
        #        if range_position.x == defending_ship_position.x and range_position.y == defending_ship_position.y:
        if not self.has_missed():
            damage = attacking_ship.fire_power() + attacking_ship.get_damage_increase()
            attacking_ship.increase_experience()
            if attacking_ship.next_level_ready():
                attacking_ship.increase_experience_level()
            attacking_ship.save()
            defending_ship.get_hurt(damage)
            defending_ship.save()
            if not defending_ship.game_player.has_ships():
                defending_ship.game_player.lost = True
                defending_ship.game_player.save()
            return OutputMessage("Ship hit with " + str(damage), MessageType.FIRE_SUCCESS)
        else:
            return OutputMessage("Missed shot!", MessageType.FIRE_MISS)
        #return OutputMessage("Ship not within range!", MessageType.FIRE_MISS)

    def has_missed(self)-> bool:
        missed = random.randrange(0, MISS_CHANCE_VALUE)
        if missed == MISS_VALUE:
            return True
        else:
            return False

    def is_game_finished(self)->bool:
        return self.winner is not None

    def is_max_players(self)-> bool:
        if self.gameplayer_set.all().exists():
            return self.gameplayer_set.count() == self.max_players
        return False

    def get_players_count(self)-> int:
        return self.gameplayer_set.count()

    def all_players_ready(self):
        return self.gameplayer_set.count() == self.max_players
