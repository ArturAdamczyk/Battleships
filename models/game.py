from django.db import models
from battleships.models.ship import Move
import json


class FireResult:
    HIT = "MOVE"
    FIRE = "FIRE"
    PASS = "PASS"
    MESSAGE = "MESSAGE"
    INVALID = "INVALID"


class Commands:
    MOVE = "MOVE"
    FIRE = "FIRE"
    PASS = "PASS"
    MESSAGE = "MSG"
    INVALID = "INVALID"


class Message():
    command = Commands.MESSAGE
    user_id = ""
    text = ""
    user_name = ""

    #def __init__(self, text):
    #    self.text = text

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class FireMessage(Message):
    command = Commands.FIRE
    attacker = ""
    defender = ""

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class MoveMessage(Message):
    command = Commands.MOVE
    mover = ""
    move_type = Move.FORWARD

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class IdleMessage(Message):
    command = Commands.PASS

    #def __init__(self):
    #    super(IdleMessage, self).__init__()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class InvalidMessage(Message):
    command = Commands.INVALID

   # def __init__(self, text):
   #    super(InvalidMessage, self).__init__(text)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class MessageType:
    MOVE_SUCCESS = "MOVE SUCCESS"
    MOVE_FAILURE = "MOVE FAILURE"
    FIRE_SUCCESS = "FIRE SUCCESS"
    FIRE_MISS = "FIRE MISS"
    FIRE_FAILURE = "FIRE FAILURE"
    GAME_END = "GAME END"
    GAME_BEGIN = "GAME BEGIN"
    GAME_FINISHED = "GAME FINISHED"
    NEW_PLAYER = "NEW PLAYER"
    NEXT_ROUND = "NEXT ROUND"
    PLAYER_ADDITION_SUCCESS = "PLAYER ADDITION SUCCESS"
    PLAYER_ADDITION_FAILURE = "PLAYER ADDITION FAILURE"
    PASS_ROUND = "PASS ROUND"
    MESSAGE = "MESSAGE"
    BAD_FORMAT = "BAD FORMAT"


class OutputMessage:
    message = ""
    message_type = MessageType
    receiver = ""  # if set than message is directed only to the specified player


# create GameMessage with result string from move and fire funcs
class Game(models.Model):
    winner = models.OneToOneField('GamePlayer', on_delete='cascade', default=None, blank=True, null=True)
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
        self.check_game_finish()
        self.refresh_game_status()
        if self.winner is None:
            return self.next_round()
        else:
            return OutputMessage("Game finished, player " + self.winner.name + " won!", MessageType.GAME_END, self.winner.id)

    def refresh_game_status(self):
        lost_players = 0
        winner = None
        for player in self.gameplayer_set:
            if player.lost:
                lost_players += 1
            else:
                winner = player
        if self.max_players - lost_players == 0:
            self.winner = winner
            self.gameplayer_set.get(self.winner).increase_score()

    def next_round(self)-> OutputMessage:
        counter = 0
        for player in self.gameplayer_set:
            if player.inControl():
                player_in_control = self.gameplayer_set.get(counter + 1)
                player_in_control.inControl = True
                self.gameplayer_set.get(counter).inControl = False
                return OutputMessage(
                    "Next round: Player " +
                    player_in_control.username +
                    " in control",
                    MessageType.NEXT_ROUND,
                    player_in_control.id)
            counter += 1

    def get_player_in_control(self):
        for player in self.gameplayer_set:
            if player.inControl:
                return player

    def move_ship(self, user, ship_name, direction)-> OutputMessage:
        self.check_game_finish()
        ship = self.objects.get(user).find_ship(ship_name)
        if ship is None:
            return OutputMessage("Not found", MessageType.MOVE_FAILURE)
        # ship_positions_after_move = ship.get_position_after_move()
        # check if no other ship blocks movement
        for user in self.objects:
            if not user.is_move_possible(ship, direction): # todo send board size in order to check also if ship will fit the board after move!
                return OutputMessage("Move not possible", MessageType.MOVE_FAILURE)
        ship.move(direction)
        return OutputMessage("Ship moved!", MessageType.MOVE_SUCCESS)

    def fire_ship(self, attacking_user, attacking_ship_name, defending_ship_name)-> OutputMessage:
        self.check_game_finish()
        defending_ship = None
        for game_player in self.gameplayer_set:
            defending_ship = game_player.find_ship(defending_ship_name)
            if defending_ship is not None:
                break
        attacking_ship = self.gameplayer_set.get(attacking_user).find_ship(attacking_ship_name)
        if defending_ship is None or attacking_ship is None:
            return OutputMessage("Not found", MessageType.FIRE_FAILURE)

        attacking_ship_visible_positions = attacking_ship.get_visibility_range_coordinates()
        # if at least one part[position] of defending ship is visible by the attacking ship -> than fire
        for range_position in attacking_ship_visible_positions:
            for defending_ship_position in defending_ship.objects:
                if range_position.x == defending_ship_position.x and range_position.y == defending_ship_position.y:
                    if not self.has_missed():
                        damage = self.count_hit_power()
                        defending_ship.get_hurt(damage)
                        return OutputMessage("Ship hit with " + damage, MessageType.FIRE_SUCCESS)
                    else:
                        return OutputMessage("Missed shot!", MessageType.FIRE_MISS)
                    break
        return OutputMessage("Ship not within range!", MessageType.FIRE_MISS)

    # def check_move_possibility(self)-> bool:
    #    pass

    def count_hit_power(self)-> int:
        pass

    def has_missed(self)-> bool:
        pass

    def check_game_finish(self)->OutputMessage:
        if self.winner is not None:
            return OutputMessage("Cannot perform action, game already finished!", MessageType.GAME_FINISHED)

    def is_max_players(self)-> bool:
        if self.gameplayer_set.all().exists():
            return self.gameplayer_set.count() == self.max_players
        return False

    def get_players_count(self)-> int:
        return self.gameplayer_set.count()
