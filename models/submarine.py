from battleships.models.ship import Ship, Move
from django.contrib.postgres.fields import ArrayField
from django.db.models import OneToOneField, CASCADE
import copy


class Submarine(Ship):

    def max_strength(self):
        return 40

    def fire_power(self):
        return 20

    def move(self, move):
        coordinate_1 = self.coordinate_set.filter()[:1].get()
        if Move(move) == Move.FORWARD:
            coordinate_1.y = coordinate_1.y + 2
        elif Move(move) == Move.BACKWARD:
            coordinate_1.y = coordinate_1.y - 2
        elif Move(move) == Move.RIGHT:
            coordinate_1.x = coordinate_1.x + 2
        elif Move(move) == Move.LEFT:
            coordinate_1.x = coordinate_1.x - 2
        else:
            pass
        coordinate_1.save()

    def get_position_after_move(self, move):
        ship_positions_after_move = list(copy.deepcopy(self.coordinate_set.all()))
        position_1 = ship_positions_after_move[0]
        if Move(move) == Move.FORWARD:
            position_1.y = position_1.y + 2
        elif Move(move) == Move.BACKWARD:
            position_1.y = position_1.y - 2
        elif Move(move) == Move.RIGHT:
            position_1.x = position_1.x + 2
        elif Move(move) == Move.LEFT:
            position_1.x = position_1.x - 2
        else:
            pass
        return [position_1]

