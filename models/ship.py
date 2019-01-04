from django.db import models
from polymorphic.models import PolymorphicModel
from enum import Enum
from typing import List
from battleships.utils.enum_utils import ChoiceEnum


class Move(Enum):
    FORWARD = "f"
    BACKWARD = "b"
    RIGHT = "r"
    LEFT = "l"


class Experience(ChoiceEnum):
    RECRUIT = "RECRUIT"
    SOLDIER = "SOLDIER"
    VETERAN = "VETERAN"


class ExperienceLevel(Enum):
    RECRUIT = 0
    SOLDIER = 100
    VETERAN = 250


class Ship(PolymorphicModel):
    name = models.CharField(max_length=200, default='')
    strength = models.IntegerField(default=0)
    experience = models.CharField(max_length=20, choices=Experience.choices(), default=Experience.RECRUIT.value)
    experience_points = models.IntegerField(default=0)
    visibility_radius = models.IntegerField(default=0)
    game_player = models.ForeignKey(to='GamePlayer', on_delete=models.CASCADE, default=None, blank=True, null=True)  # todo delete nulls

    class Meta:
        abstract = True

    def max_strength(self):
        pass

    def fire_power(self):
        pass

    # zwrocic liste koordynatów na podstawie radiusa które statek 'widzi' (pozniej obciac te ktore poza macierza!
    def get_visibility_range_coordinates(self):
        visibility_coordinates = list()
        #visibility_coordinates.append(Coordinate(1, 2))
        return visibility_coordinates

    def move(self, move)-> bool:
        pass

    # todo ; when implemented then also move method must be changed
    def rotation(self, move: Move)-> bool:
        pass

    def get_position_after_move(self, move):
        pass

    def next_level_ready(self) -> bool:
        if self.experience == Experience.RECRUIT and self.experience_points >= ExperienceLevel.SOLDIER.value:
            self.experience = Experience.SOLDIER
            return True
        elif self.experience == Experience.SOLDIER and self.experience_points >= ExperienceLevel.RECRUIT.value:
            self.experience = ExperienceLevel.VETERAN
            return True
        else:
            return False

    def increase_experience_level(self):
        if self.experience == ExperienceLevel.RECRUIT:
            self.experience = ExperienceLevel.SOLDIER
        elif self.experience == ExperienceLevel.SOLDIER:
            self.experience = ExperienceLevel.VETERAN
        else:
            pass

    def get_hurt(self, how_much: int):
        self.strength -= how_much

    def is_sunk(self) -> bool:
        return self.strength <= 0








