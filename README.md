# Battleships
Multiplayer battleships game.

Created with Python 3.7.1 Django 2.1.4 + PostgreSQL 11.1 + JavaScript

Multiplayer ability is based on WebSocket concept (Django channels)

All players share one board and each one of them has it`s own ship set.
In order to win the game shoot down all enemies ships and don`t let your ships sunk.
The game is turn-based - when your turn comes you have three options: fire to enemy ship, move one of your ships or skip your turn.
You can control the game by typing these commands:

MOVE:
MOVE ship_name [LEFT, RIGHT, BACKWARD, FORWARD]

FIRE:
FIRE ship_name TO ship_name

SKIP:
PASS

MESSAGE:
MSG message



#Work in progress...