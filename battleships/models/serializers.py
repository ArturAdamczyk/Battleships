from rest_framework import serializers
from battleships.models.game import Game
from battleships.models.game_player import GamePlayer
from battleships.models.ship import Ship
from battleships.models.coordinate import Coordinate


class CoordinateSerializer(serializers.Serializer):
    x = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    y = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    carrier = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    destroyer = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    frigate = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    submarine = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Coordinate
        fields = '__all__'


class ShipSerializer(serializers.Serializer):
    game_player = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    name = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    strength = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    experience = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    experience_points = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    visibility_radius = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    coordinate_set = CoordinateSerializer(many=True)

    class Meta:
        model = Ship
        fields = '__all__'
        abstract = True


class GamePlayerSerializer(serializers.ModelSerializer):
    game = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    player = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    carrier_set = ShipSerializer(many=True)
    frigate_set = ShipSerializer(many=True)
    destroyer_set = ShipSerializer(many=True)
    submarine_set = ShipSerializer(many=True)

    class Meta:
        model = GamePlayer
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    gameplayer_set = GamePlayerSerializer(many=True)

    class Meta:
        model = Game
        fields = '__all__'




