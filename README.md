# Battleships
Multiplayer battleships game.

Created with Python 3.7.1 + Django 2.1.4 + PostgreSQL 11.1 + JavaScript

Multiplayer ability is based on WebSocket concept (Django channels)

All players[max 4, min 2] share one board and each one of them has it`s own ship set.
In order to win the game shoot down all enemies ships and don`t let your ships sunk.
The game is turn-based - when your turn comes you have three options: fire to enemy ship, move one of your ships or skip your turn.
You can control the game by typing these commands:

MOVE:
move ship_name [left, right, back, forth]

FIRE:
fire ship_name at ship_name

SKIP:
pass

MESSAGE:
msg message



<div align="center">
    <img src="/screenshot.jpg"</img> 
</div>




Setup:


clone repository  
install python 3.7.1  
install postgreSQL  
install pgAdmin4  
launch pgadmin4 -> create new server -> create new db called battleships  
[*]  
open cmd in the cloned repo folder  
type:  
install pip -r requirements.txt  
python manage.py makemigrations  
python manage.py migrate  
python manage.py runserver  

your game is now available on 127.0.0.1:8000, enjoy!  

[*] installation of visual studio c++ build tools 2017 might be needed  




#Work in progress...  
