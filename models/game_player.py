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
        for ship in self.objects:
            if ship.name == name:
                return ship

    def increase_score(self):
        self.player.score += SCORE_INCREASE_VALUE

    # it would be better to store the whole board in game with enum types and just check it out there
    def is_move_possible(self, moving_ship, direction)-> bool:
        ship_positions_after_move = moving_ship.get_position_after_move(direction)
        # todo first check if board is not exceeded!
        # check if there is no other ship on this position
        for ship in self.objects:
            for ship_position in ship.objects:
                for position in ship_positions_after_move:
                    if ship_position.x == position.x and ship_position.y == position.y and ship.name != moving_ship.name:
                        return False
        return True

    def move_ship(self)->bool:
        pass

    def attach_ships(self, ships):
        for ship in ships:
            ship.game_player = self
            ship.save()
