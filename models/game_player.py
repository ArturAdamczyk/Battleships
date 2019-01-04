from django.db import models
from battleships.models.ship import Ship
from battleships.models.player import Player

SCORE_INCREASE_VALUE = 100


class GamePlayer(models.Model):
    ready = models.BooleanField(default=False)
    lost = models.BooleanField(default=False)
    inControl = models.BooleanField(default=False)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(to='Game', on_delete=models.CASCADE)

    def find_ship(self, name)-> Ship:
        #could also be:
        #ship = self.carrier_set.get(name=name)
        for ship in self.carrier_set.all():
            if ship.name == name:
                return ship
        for ship in self.destroyer_set.all():
            if ship.name == name:
                return ship
        for ship in self.frigate_set.all():
            if ship.name == name:
                return ship
        for ship in self.submarine_set.all():
            if ship.name == name:
                return ship

    def increase_score(self):
        self.player.score += SCORE_INCREASE_VALUE

    # it would be better to store the whole board in game with enum types and just check it out there
    def is_move_possible(self, moving_ship, direction, board_size)-> bool:
        ship_positions_after_move = moving_ship.get_position_after_move(direction)
        # first check if board is not exceeded!
        for position in ship_positions_after_move:
            if position.x > board_size or position.x <= 1 or position.y > board_size or position.y <= 1:
                return False

        # check if there is no other ship on this position
        for ship in self.carrier_set.all():
            for ship_position in ship.coordinate_set.all():
                for position in ship_positions_after_move:
                    if ship_position.x == position.x and ship_position.y == position.y and ship.id != moving_ship.id:
                        return False
        for ship in self.frigate_set.all():
            for ship_position in ship.coordinate_set.all():
                for position in ship_positions_after_move:
                    if ship_position.x == position.x and ship_position.y == position.y and ship.id != moving_ship.id:
                        return False
        for ship in self.destroyer_set.all():
            for ship_position in ship.coordinate_set.all():
                for position in ship_positions_after_move:
                    if ship_position.x == position.x and ship_position.y == position.y and ship.id != moving_ship.id:
                        return False
        for ship in self.submarine_set.all():
            for ship_position in ship.coordinate_set.all():
                for position in ship_positions_after_move:
                    if ship_position.x == position.x and ship_position.y == position.y and ship.id != moving_ship.id:
                        return False
        return True

    def move_ship(self)->bool:
        pass

    def attach_ships(self, ships):
        for ship in ships:
            ship.game_player = self
            ship.save()
