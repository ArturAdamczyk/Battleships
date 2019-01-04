from battleships.models.ship import Ship, Move
import copy


class Frigate(Ship):

    def max_strength(self):
        return 50

    def fire_power(self):
        return 5

    def move(self, move):
        coordinates = self.coordinate_set.all()
        if Move(move) == Move.FORWARD:
            for coordinate in coordinates:
                coordinate.y = coordinate.y + 3
        elif Move(move) == Move.BACKWARD:
            for coordinate in coordinates:
                coordinate.y = coordinate.y - 3
        elif Move(move) == Move.RIGHT:
            for coordinate in coordinates:
                coordinate.x = coordinate.x + 3
        elif Move(move) == Move.LEFT:
            for coordinate in coordinates:
                coordinate.x = coordinate.x - 3
        else:
            pass
        for coordinate in coordinates:
            coordinate.save()

    def get_position_after_move(self, move):
        ship_positions_after_move = list(copy.deepcopy(self.coordinate_set.all()))
        position_1 = ship_positions_after_move[0]
        position_2 = ship_positions_after_move[1]
        if Move(move) == Move.FORWARD:
            position_1.y = position_1.y + 3
            position_2.y = position_2.y + 3
        elif Move(move) == Move.BACKWARD:
            position_1.y = position_1.y - 3
            position_2.y = position_2.y - 3
        elif Move(move) == Move.RIGHT:
            position_1.x = position_1.x + 3
            position_2.x = position_2.x + 3
        elif Move(move) == Move.LEFT:
            position_1.x = position_1.x - 3
            position_2.x = position_2.x - 3
        else:
            pass
        return [position_1, position_2]
