from battleships.models.ship import Ship, Move

from django.db import models

from django.contrib.postgres.fields import ArrayField
from django.db.models import OneToOneField, CASCADE
import copy


class Carrier(Ship):

    def max_strength(self):
        return 100

    def fire_power(self):
        return 10

    def move(self, move: Move):
        if move == Move.FORWARD:
            self.coordinate_set.get(1).y = self.coordinate_set.get(1).y + 1
            self.coordinate_set.get(2).y = self.coordinate_set.get(2).y + 1
            self.coordinate_set.get(3).y = self.coordinate_set.get(3).y + 1
            self.coordinate_set.get(4).y = self.coordinate_set.get(4).y + 1
        elif move == Move.BACKWARD:
            self.coordinate_set.get(1).y = self.coordinate_set.get(1).y - 1
            self.coordinate_set.get(2).y = self.coordinate_set.get(2).y - 1
            self.coordinate_set.get(3).y = self.coordinate_set.get(3).y - 1
            self.coordinate_set.get(4).y = self.coordinate_set.get(4).y - 1
        elif move == Move.RIGHT:
            self.coordinate_set.get(1).x = self.coordinate_set.get(1).x + 1
            self.coordinate_set.get(2).x = self.coordinate_set.get(2).x + 1
            self.coordinate_set.get(3).x = self.coordinate_set.get(3).x + 1
            self.coordinate_set.get(4).x = self.coordinate_set.get(4).x + 1
        elif move == Move.LEFT:
            self.coordinate_set.get(1).x = self.coordinate_set.get(1).x - 1
            self.coordinate_set.get(2).x = self.coordinate_set.get(2).x - 1
            self.coordinate_set.get(3).x = self.coordinate_set.get(3).x - 1
            self.coordinate_set.get(4).x = self.coordinate_set.get(4).x - 1
        else:
            pass

    def get_position_after_move(self, move: Move) -> list:
        ship_positions_after_move = copy.deepcopy(self.coordinate_set)
        if move == Move.FORWARD:
            ship_positions_after_move[1].y = ship_positions_after_move[1].y + 1
            ship_positions_after_move[2].y = ship_positions_after_move[2].y + 1
            ship_positions_after_move[3].y = ship_positions_after_move[3].y + 1
            ship_positions_after_move[4].y = ship_positions_after_move[4].y + 1
        elif move == Move.BACKWARD:
            ship_positions_after_move[1].y = ship_positions_after_move[1].y - 1
            ship_positions_after_move[2].y = ship_positions_after_move[2].y - 1
            ship_positions_after_move[3].y = ship_positions_after_move[3].y - 1
            ship_positions_after_move[4].y = ship_positions_after_move[4].y - 1
        elif move == Move.RIGHT:
            ship_positions_after_move[1].x = ship_positions_after_move[1].x + 1
            ship_positions_after_move[2].x = ship_positions_after_move[2].x + 1
            ship_positions_after_move[3].x = ship_positions_after_move[3].x + 1
            ship_positions_after_move[4].x = ship_positions_after_move[4].x + 1
        elif move == Move.LEFT:
            ship_positions_after_move[1].x = ship_positions_after_move[1].x - 1
            ship_positions_after_move[2].x = ship_positions_after_move[2].x - 1
            ship_positions_after_move[3].x = ship_positions_after_move[3].x - 1
            ship_positions_after_move[4].x = ship_positions_after_move[4].x - 1
        else:
            pass
