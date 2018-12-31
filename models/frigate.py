from battleships.models.ship import Ship, Move
import copy


class Frigate(Ship):

    def max_strength(self):
        return 50

    def fire_power(self):
        return 5

    def move(self, move: Move):
        self.calculate_positions(self.shipPositions, move)

    def get_position_after_move(self, move: Move) -> list:
        ship_positions_after_move = copy.deepcopy(self.shipPositions)
        return self.calculate_positions(ship_positions_after_move, move)

    @staticmethod
    def calculate_positions(ship_positions, move: Move)-> list:
        if move == Move.FORWARD:
            ship_positions[1].y = ship_positions[1].y + 3
            ship_positions[2].y = ship_positions[2].y + 3
        elif move == Move.BACKWARD:
            ship_positions[1].y = ship_positions[1].y - 3
            ship_positions[2].y = ship_positions[2].y - 3
        elif move == Move.RIGHT:
            ship_positions[1].x = ship_positions[1].x + 3
            ship_positions[2].x = ship_positions[2].x + 3
        elif move == Move.LEFT:
            ship_positions[1].x = ship_positions[1].x - 3
            ship_positions[2].x = ship_positions[2].x - 3
        else:
            pass