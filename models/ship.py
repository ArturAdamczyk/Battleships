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
    SOLDIER = 50
    VETERAN = 70


class Ship(PolymorphicModel):
    EXPERIENCE_LEVEL_INCREASE = 50

    name = models.CharField(max_length=200, default='')
    strength = models.IntegerField(default=0)
    experience = models.CharField(max_length=20, choices=Experience.choices(), default=Experience.RECRUIT.value)
    experience_points = models.IntegerField(default=0)
    visibility_radius = models.IntegerField(default=0)
    game_player = models.ForeignKey(to='GamePlayer', on_delete=models.CASCADE, default=None, blank=True, null=True)  # todo delete nulls

    class Meta:
        abstract = True

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
        if Experience(self.experience) == Experience.RECRUIT and self.experience_points >= ExperienceLevel.SOLDIER.value:
            return True
        elif Experience(self.experience) == Experience.SOLDIER and self.experience_points >= ExperienceLevel.VETERAN.value:
            return True
        else:
            return False

    def increase_experience_level(self):
        if Experience(self.experience) == Experience.RECRUIT:
            self.experience = Experience.SOLDIER.value
        elif Experience(self.experience) == Experience.SOLDIER:
            self.experience = Experience.VETERAN.value
        else:
            pass

    def get_damage_increase(self):
        if Experience(self.experience) == Experience.RECRUIT:
            return 0
        elif Experience(self.experience) == Experience.SOLDIER:
            return 10
        else:
            return 25

    def increase_experience(self):
        self.experience_points += Ship.EXPERIENCE_LEVEL_INCREASE

    def get_hurt(self, how_much):
        self.strength -= how_much

    def is_sunk(self) -> bool:
        return self.strength <= 0








