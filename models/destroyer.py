from battleships.models.ship import Ship, Move
import copy


class Destroyer(Ship):

    def max_strength(self):
        return 80

    def fire_power(self):
        return 15

    def move(self, move: Move):
        if move == Move.FORWARD:
            self.shipPositions[1].y = self.shipPositions[1].y + 2
            self.shipPositions[2].y = self.shipPositions[2].y + 2
            self.shipPositions[3].y = self.shipPositions[3].y + 2
        elif move == Move.BACKWARD:
            self.shipPositions[1].y = self.shipPositions[1].y - 2
            self.shipPositions[2].y = self.shipPositions[2].y - 2
            self.shipPositions[3].y = self.shipPositions[3].y - 2
        elif move == Move.RIGHT:
            self.shipPositions[1].x = self.shipPositions[1].x + 1
            self.shipPositions[2].x = self.shipPositions[2].x + 1
            self.shipPositions[3].x = self.shipPositions[3].x + 1
        elif move == Move.LEFT:
            self.shipPositions[1].x = self.shipPositions[1].x - 1
            self.shipPositions[2].x = self.shipPositions[2].x - 1
            self.shipPositions[3].x = self.shipPositions[3].x - 1
        else:
            pass

    def get_position_after_move(self, move: Move) -> list:
        ship_positions_after_move = copy.deepcopy(self.shipPositions)
        if move == Move.FORWARD:
            ship_positions_after_move[1].y = ship_positions_after_move[1].y + 2
            ship_positions_after_move[2].y = ship_positions_after_move[2].y + 2
            ship_positions_after_move[3].y = ship_positions_after_move[3].y + 2
        elif move == Move.BACKWARD:
            ship_positions_after_move[1].y = ship_positions_after_move[1].y - 2
            ship_positions_after_move[2].y = ship_positions_after_move[2].y - 2
            ship_positions_after_move[3].y = ship_positions_after_move[3].y - 2
        elif move == Move.RIGHT:
            ship_positions_after_move[1].x = ship_positions_after_move[1].x + 1
            ship_positions_after_move[2].x = ship_positions_after_move[2].x + 1
            ship_positions_after_move[3].x = ship_positions_after_move[3].x + 1
        elif move == Move.LEFT:
            ship_positions_after_move[1].x = ship_positions_after_move[1].x - 1
            ship_positions_after_move[2].x = ship_positions_after_move[2].x - 1
            ship_positions_after_move[3].x = ship_positions_after_move[3].x - 1
        else:
            pass