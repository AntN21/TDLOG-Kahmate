var socket = io.connect()
var players = ["clever_red", "strong_red", "tough_red", "fast_red", "ordinary_red", "ko_red",
                "clever_blue", "strong_blue", "tough_blue", "fast_blue", "ordinary_blue","ko_blue"];

var BOARD_WIDTH = 13
var BOARD_HEIGHT = 8

function get_src(player) {
    /**
     *   Returns the player's png image path
     */
    return "../static/images/" + player + ".png";
}

function updateBoard(board) {
    /**
     *   Updates the board squares from a board json object.
     */

    for (let row = 0; row < BOARD_HEIGHT; row++) {
        for (let col = 0; col < BOARD_WIDTH; col++) {
            var selected_square_element = document.getElementById('('+String(row)+', '+String(col) + ')')
            var selected_square_json = board[row * BOARD_WIDTH + col]
            var child = selected_square_element.lastElementChild; 
            while (child) {
                selected_square_element.removeChild(child);
                child = selected_square_element.lastElementChild;
            }
            if(selected_square_json.ball) {
                var image = document.createElement("img");
                image.src = get_src("ball");
                image.draggable = false;
                image.style.top = "20px";
                image.style.left = "20px";
                image.style.position = "absolute";
                image.style.width = "40px";
                image.style.width = "40px";
                selected_square_element.appendChild(image);
            }
            if(selected_square_json.player) {
                var image = document.createElement("img");
                var player = selected_square_json.player
                image.src = get_src(player);
                image.draggable = false;
                image.style.width = "40px";
                image.style.width = "40px";
                selected_square_element.appendChild(image);
            }
            if(selected_square_json.available || selected_square_json.selected) {
                if(selected_square_json.available)
                    selected_square_element.style.borderColor = "white"
                if(selected_square_json.selected){
                    selected_square_element.style.borderColor = "red"
                }
            } else {
                selected_square_element.style.borderColor = "black"
            }
        }
    }
}

function clearMenu() {
    /**
     *   Turns all buttons invisible
     */
    
    document.getElementById("move").style.display = "None";
    document.getElementById("ball_kick").style.display = "None";
    document.getElementById("plackage").style.display = "None";
    document.getElementById("forced_passage").style.display = "None";
    document.getElementById("pass").style.display = "None";
    document.getElementById("next_turn").style.display = "None";

    document.getElementById("card_1").style.display = "None";
    document.getElementById("card_2").style.display = "None";
    document.getElementById("card_3").style.display = "None";
    document.getElementById("card_4").style.display = "None";
    document.getElementById("card_5").style.display = "None";
    document.getElementById("card_6").style.display = "None";
}

function updateMenu(current_game, client_team) {
    /**
     *   Show all menu buttons that are available in the current game for the designated team
     */
    document.getElementById("turn_card").style.backgroundColor = current_game.team_playing;
    document.getElementById("turn_text").innerHTML = "It is " + current_game.team_playing + "'s turn";
    clearMenu()
    console.log(current_game);
    if(current_game.team_playing == client_team) {
        document.getElementById("next_turn").style.display = "inline";

        console.log(current_game.actions);
        console.log("Selected case:", current_game.selected_case);
        var selected_case = current_game.selected_case;
        if(selected_case != null) {
            for(i in current_game.actions) {

                action = current_game.actions[i]
                if(action.position_1[0] == selected_case[0] &&
                    action.position_1[1] == selected_case[1]) {
                    if(action.type == "Move")
                        document.getElementById("move").style.display = "inline";
                    if(action.type == "Pass")
                        document.getElementById("pass").style.display = "inline";
                    if(action.type == "BallKick")
                        document.getElementById("ball_kick").style.display = "inline";
                    if(action.type == "Plackage")
                       document.getElementById("plackage").style.display = "inline";
                }
            }
        }
        

        //Check if there is a selected case
        if(current_game._selected_case != null) {

            //Check if the selected player can move
            if(current_game._selected_case._player._available_moves > 0) {
                document.getElementById("move").style.display = "inline";
            }
    
            //Check if the selected player can force its passage
            if(false/* It has an opposite team player next to itself and move > 1*/) {
                document.getElementById("forced_passage").style.display = "inline";
            }
    
            //Check if the selected player can pass or kick the ball
            if(current_game._selected_case._ball) {
                document.getElementById("pass").style.display = "inline";
    
                if(true/* If it is the most advanced player */)
                    document.getElementById("ball_kick").style.display = "inline";
            }
        }
    }

    if(current_game.duel != null) {
        clearMenu();
        var cards = current_game.team_playing == client_team.team_json ? 
                    current_game.duel.player_1_cards :
                    current_game.duel.player_2_cards;
        for(let i = 0; i < cards.length; i++) {
            document.getElementById("card_" + cards[i]).style.display = "inline";
        }
    }
}

function updateGameInfo(current_game, client_team) {
    /**
     *   Updates all game info shown (current player's turn, available moves, available cards)
     */
    document.getElementById("player_info_card").style.backgroundColor = client_team;
    document.getElementById("player_red_custom_name").innerHTML = current_game.team_red.custom_name;
    document.getElementById("player_blue_custom_name").innerHTML = current_game.team_blue.custom_name;
    var team = client_team == "red" ? current_game.team_red : current_game.team_blue; 
    document.getElementById("player_moves_left").innerHTML = "Selected?";
    document.getElementById("team_moves_left").innerHTML = "Moves left: " + team.moves_left;
    document.getElementById("cards_left").innerHTML = "Cards left: " + team.cards;
    
}

function updateGame(current_game, team) {
    this.current_game = JSON.parse(current_game);
    updateBoard(this.current_game.board)
    updateGameInfo(this.current_game, team)
    updateMenu(this.current_game, team)
    document.getElementById("all").style.display = "flex";
}

socket.on("updateBoard", function (data) {
    this.current_game = JSON.parse(data.current_game);
    updateBoard(this.current_game.board);
});

socket.on("updateMenu", function (data) {
    this.current_game = JSON.parse(data.current_game);
    updateMenu(this.current_game, this.current_game.team_playing);
});

socket.on("updateGameInfo", function(data) {
    this.current_game = JSON.parse(data.current_game);
    updateGameInfo(this.current_game, this.current_game.team_playing);
})
