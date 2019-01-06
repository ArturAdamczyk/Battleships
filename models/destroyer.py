from battleships.models.ship import Ship, Move
import copy


class Destroyer(Ship):

    MAX_STRENGTH = 80
    VISIBILITY_RADIUS_MULTIPLIER = 0.3

    def fire_power(self):
        return 15

    def move(self, move):
        coordinates = self.coordinate_set.all()
        if Move(move) == Move.FORWARD:
            for coordinate in coordinates:
                coordinate.y = coordinate.y + 2
        elif Move(move) == Move.BACKWARD:
            for coordinate in coordinates:
                coordinate.y = coordinate.y - 2
        elif Move(move) == Move.RIGHT:
            for coordinate in coordinates:
                coordinate.x = coordinate.x + 1
        elif Move(move) == Move.LEFT:
            for coordinate in coordinates:
                coordinate.x = coordinate.x - 1
        else:
            pass
        for coordinate in coordinates:
            coordinate.save()

    def get_position_after_move(self, move):
        ship_positions_after_move = list(copy.deepcopy(self.coordinate_set.all()))
        position_1 = ship_positions_after_move[0]
        position_2 = ship_positions_after_move[1]
        position_3 = ship_positions_after_move[2]
        if Move(move) == Move.FORWARD:
            position_1.y = position_1.y + 2
            position_2.y = position_2.y + 2
            position_3.y = position_3.y + 2
        elif Move(move) == Move.BACKWARD:
            position_1.y = position_1.y - 2
            position_2.y = position_2.y - 2
            position_3.y = position_3.y - 2
        elif Move(move) == Move.RIGHT:
            position_1.x = position_1.x + 1
            position_2.x = position_2.x + 1
            position_3.x = position_3.x + 1
        elif Move(move) == Move.LEFT:
            position_1.x = position_1.x - 1
            position_2.x = position_2.x - 1
            position_3.x = position_3.x - 1
        else:
            pass
        return [position_1, position_2, position_3]
