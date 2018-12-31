var url = window.location.href;
var webSocketStarted = false;
const KEY_ENTER = 13;
// user_id is a globally accessible variable instantiated in game.html

// 'main' func invoked on page load
$(document).ready(function() {
    setupChatMessageListener(document.getElementById("user_input"));
    joinGame(url + "/join")
        .then(response => {
            console.log(response);
            if(response.status == 200){
                loadGame();
            }
            response.json().then(function(object) {

            })
        })
        .catch(error => console.log(error))
});

function loadGame(){
   fetchGameData(url + "/refresh")
        .then(response => {
            refreshUI(response);
            startWebSocketListener(response.id, user_id);
        })
        .catch(error => console.log(error))
}

function setupChatMessageListener(userInput){
    userInput.addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === KEY_ENTER) {
            insertChatMessage(this.value, true);
            message = serializeMessage(this.value);
            clearInput(this);
            play(url + "/play", message)
                .then(response => {
                    console.log(response);
                    if (response.status == 200) {
                        console.log("OK")
                    }
                })
                .catch(error => console.log(error))
        }
    });
}

function serializeMessage(message){
   console.log(JSON.stringify({'message': message}));
   return {
       method: 'post',
       headers: {
           'Accept': 'application/json',
           'Content-Type': 'application/json'
       },
       body: JSON.stringify({'message': message})
   };
}

function clearInput(input){
    input.value = "";
}

function insertChatMessage(message, hostMessage){
    var chat = document.getElementById("chatbox");
    var text = document.createTextNode(`${message}`);
    if(hostMessage){
        text = document.createTextNode(`you: ${message}`);
    }
    var newLine = document.createElement("br");
    chat.appendChild(text);
    chat.appendChild(newLine);
}


function refreshUI(game){
  var userIndex = getUserIndex(game.gamePlayers);
  document.getElementById('game_fleet').innerHTML = "";
  renderFleet(
      game.gamePlayers[userIndex].carriers,
      game.gamePlayers[userIndex].frigates,
      game.gamePlayers[userIndex].submarines,
      game.gamePlayers[userIndex].destroyers);
  document.getElementById("game_title").innerHTML=renderTitle(game.name);
  document.getElementById("board").innerHTML=renderBoard(game);
}


function getUserIndex(gamePlayers){
  var counter = 0;
  gamePlayers.every( gamePlayer =>{
      if(parseInt(gamePlayer.player) == parseInt(user_id)){
          return;
      }else{
          counter++;
      }
  });
  return counter;
}

function renderBoard(game){

  var board = [];

  for(var i=0; i < game.boardSize; i++){
      board.push([]);
      board[i].push( new Array(game.boardSize));
      for(var j=0; j < game.boardSize; j++){
        board[i][j] = new BoardElement(colors.BLUE, "");
      }
  }

  var playersCounter = 0;
  var color = colors.BLUE;

    game.gamePlayers.forEach(function(gamePlayer) {
        switch(playersCounter){
            case 0: color = colors.GREEN;
            case 1: color = colors.RED;
            case 2: color = colors.ORANGE;
            case 3: color = colors.PURPLE;
        }
        gamePlayer.carriers.forEach(function(carrier) {
            carrier.coordinates.forEach(function(coordinate) {
                board[game.boardSize-coordinate.y][coordinate.x-1] = new BoardElement(color, carrier.name);
            });
        });
        gamePlayer.frigates.forEach(function(frigate) {
            frigate.coordinates.forEach(function(coordinate) {
                board[game.boardSize-coordinate.y][coordinate.x-1] = new BoardElement(color, frigate.name);
            });
        });
        gamePlayer.destroyers.forEach(function(destroyer) {
            destroyer.coordinates.forEach(function(coordinate) {
                board[game.boardSize-coordinate.y][coordinate.x-1] = new BoardElement(color, destroyer.name);
            });
        });
        gamePlayer.submarines.forEach(function(submarine) {
            submarine.coordinates.forEach(function(coordinate) {
                board[game.boardSize-coordinate.y][coordinate.x-1] = new BoardElement(color, submarine.name);
            });
        });
    });

return board.map(row => row.map(col => `<span class="field ${determineColor(col.color)}">${col.name}</span>` ).join("")).join("<span class='clear'></span>");

}

function determineColor(color){
    switch(color){
        case colors.GREEN: return "team1";
        case colors.RED: return "team2";
        case colors.ORANGE: return "team3";
        case colors.PURPLE: return "team4";
        case colors.BLUE: return "sea";
    }
}

function renderFleet(carriers, frigates, submarines, destroyers){
  render_ships(carriers,"Carriers" );
  render_ships(frigates, "Frigates");
  render_ships(submarines, "Submarines");
  render_ships(destroyers, "Destroyers");
}

function render_ships(ships, ships_name){
  var listElem = document.getElementById('game_fleet');
  listElem.innerHTML += "<h4>"+ ships_name +"</h4>";
  ships.forEach(function(ship) {
    listElem.innerHTML += "<li> <b><font color=\"black\">NAME: </font></b>  " + +ship.name+  " <b><font color=\"black\"> EXP: </font></b> " + ship.experience + " <b><font color=\"black\"> STRENGTH: </font></b> " + ship.strength+ "</li>";
  });
}

function renderTitle(gameName){
    return "<b>"+gameName+"</b>"
}

function startWebSocketListener(gameId, userId){
    //var ws = new WebSocket((window.location.protocol == 'http') ? 'ws://' : 'wss://' +  window.location.host + '/game/' + gameId);
    var ws = new WebSocket('ws://'  +  window.location.host + '/game/' + gameId);
    console.log('ws://'+window.location.host + '/game/' + gameId);
    ws.id = userId;
    ws.channel = gameId;
    // Make it show an alert when a message is received
    ws.onmessage = function(message) {
        // do stuff when message received
      console.log('W' + this.id + ': ' + message.data);
      insertChatMessage('W' + this.id + ': ' + message.data, false);
      //insertChatMessage(message.data, false);
      refreshGame();
    };
    // Send a new message when the WebSocket opens
    ws.onopen = function() {
      //console.log('Hello, channel ' + this.channel + ', from id: ' + this.id);
      //this.send('Hello, channel ' + this.channel + ', from id: ' + this.id);
    };
}

function refreshGame(){
  fetchGameData(url + "/refresh")
      .then(response=>{
          refreshUI(response);
      })
      .catch(error => console.log(error))
}










// API CALLS











async function play(url, message){
  return await fetch(url, message);
}

async function joinGame (url) {
  return await fetch(url);
}

async function fetchGameData(url) {
    let response = await fetch(url);
    let data = await response.json();
    console.log(data);
    return Game.fromJson(data);
}














// MODELS


const colors = {
    GREEN: 'green',
    PURPLE: 'purple',
    RED: 'red',
    ORANGE: 'orange',
    BLUE: 'blue'
};


class BoardElement {
    constructor(color, name){
        this.color = color;
        this.name = name;
    }
}

class Game{
    constructor(id, name, boardSize, finished, maxPlayers, gamePlayers){
        this.id = id;
        this.name= name;
        this.boardSize = boardSize;
        this.finished = finished;
        this.maxPlayers = maxPlayers;
        this.gamePlayers = gamePlayers;
    }
}


Game.fromJson = function (json){
    //var obj = JSON.parse (json);
    console.log(json.name);
    //return new Game (obj.id, obj.name, obj.boardSize, obj.finished, obj.maxPlayers, GamePlayer.fromJson(obj.gameplayer_set));
    var gamePlayers = [];
    json.gameplayer_set.forEach(function(gamePlayer) {
        gamePlayers.push(GamePlayer.fromJson(gamePlayer))
    });
    return new Game (json.id, json.name, json.boardSize, json.finished, json.max_players, gamePlayers);
};


class GamePlayer{
    constructor(id, name, player, lost, ready, inControl, carriers, frigates, submarines, destroyers){
        this.id = id;
        this.name = name;
        this.player = player;
        this.lost = lost;
        this.ready = ready;
        this.inControl = inControl;
        this.carriers = carriers;
        this.frigates = frigates;
        this.submarines = submarines;
        this.destroyers = destroyers;
    }
}

GamePlayer.fromJson = function (obj){
    //var obj = JSON.parse (json);

    var carriers = [];
    obj.carrier_set.forEach(function(carrier) {
        carriers.push(Ship.fromJson(carrier))
    });
    var frigates = [];
    obj.frigate_set.forEach(function(carrier) {
        frigates.push(Ship.fromJson(carrier))
    });
    var submarines = [];
    obj.submarine_set.forEach(function(submarine) {
        submarines.push(Ship.fromJson(submarine))
    });
    var destroyers = [];
    obj.destroyer_set.forEach(function(destroyer) {
        destroyers.push(Ship.fromJson(destroyer))
    });
    return new GamePlayer(obj.id, obj.name, obj.player, obj.lost, obj.ready, obj.inControl, carriers, frigates, submarines, destroyers);
};


class Ship{
    constructor(id, name, strength, experience, experiencePoints, coordinates){
        this.id = id;
        this.name = name;
        this.strength = strength;
        this.experience = experience,
        this.experiencePoints = experiencePoints;
        this.coordinates = coordinates;
    }
}

Ship.fromJson = function (obj){
    var coordinates = [];
    obj.coordinate_set.forEach(function(coordinate) {
        coordinates.push(Coordinate.fromJson(coordinate))
    });
    return new Ship(obj.id, obj.name, obj.strength, obj.experience, obj.experiencePoints, coordinates);
};


class Coordinate{
    constructor(x,y){
        this.x = x;
        this.y = y;
    }
}

Coordinate.fromJson = function (obj){
    return new Coordinate(obj.x, obj.y);
};
