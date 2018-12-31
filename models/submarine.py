from battleships.models.ship import Ship, Move
from django.contrib.postgres.fields import ArrayField
from django.db.models import OneToOneField, CASCADE
import copy


class Submarine(Ship):

    def max_strength(self):
        return 40

    def fire_power(self):
        return 20

    def move(self, move: Move):
        if move == Move.FORWARD:
            self.shipPositions[1].y = self.shipPositions[1].y + 2
        elif move == move.BACKWARD:
            self.shipPositions[1].y = self.shipPositions[1].y - 2
        elif move == move.RIGHT:
            self.shipPositions[1].x = self.shipPositions[1].x + 2
        elif move == move.LEFT:
            self.shipPositions[1].x = self.shipPositions[1].x - 2
        else:
            pass

    def get_position_after_move(self, move: Move) -> list:
        ship_positions_after_move = copy.deepcopy(self.shipPositions)
        if move == Move.FORWARD:
            ship_positions_after_move[1].y = ship_positions_after_move[1].y + 2
        elif move == Move.BACKWARD:
            ship_positions_after_move[1].y = ship_positions_after_move[1].y - 2
        elif move == Move.RIGHT:
            ship_positions_after_move[1].x = ship_positions_after_move[1].x + 2
        elif move == Move.LEFT:
            ship_positions_after_move[1].x = ship_positions_after_move[1].x - 2
        else:
            pass
