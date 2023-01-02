var socket = io.connect()
var players = ["clever_red", "strong_red", "tough_red", "fast_red", "ordinary_red", "ko_red",
                "clever_blue", "strong_blue", "tough_blue", "fast_blue", "ordinary_blue","ko_blue"];

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

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 11; col++) {
            var selected_square_element = document.getElementById('('+String(row)+', '+String(col) + ')')
            var selected_square_json = board[row * 11 + col]
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
                selected_chip.appendChild(image);
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

function updateMenu(current_game, team) {
    /**
     *   Show all menu buttons that are available in the current game for the designated team
     */
    document.getElementById("turn_card").style.backgroundColor = current_game.team_playing;
    document.getElementById("turn_text").innerHTML = "It is " + current_game.team_playing + "'s turn";
    clearMenu()
    if(current_game.team_playing == team.team) {
        document.getElementById("next_turn").style.display = "inline";

        console.log(current_game.actions)

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

    if(current_game._duel) {
        //Here it should only show the available cards for X team
        document.getElementById("card_1").style.display = "inline";
        document.getElementById("card_2").style.display = "inline";
        document.getElementById("card_3").style.display = "inline";
        document.getElementById("card_4").style.display = "inline";
        document.getElementById("card_5").style.display = "inline";
        document.getElementById("card_6").style.display = "inline";
    }
    //if(current_game._selected_case._player)
}

function updateGameInfo(current_game, player) {
    /**
     *   Updates all game info shown (current player's turn, available moves, available cards)
     */
    document.getElementById("player_info_card").style.backgroundColor = player.team;
}

function updateGame(current_game, team) {
    updateBoard(current_game.board)
    updateGameInfo(current_game, team)
    updateMenu(current_game, team)
}

socket.on("updateBoard", function (data) {
    this.current_game = JSON.parse(data.current_game);
    updateBoard(this.current_game.board);
});

socket.on("updateMenu", function (data) {
    this.current_game = JSON.parse(data.current_game);
    updateMenu(this.current_game, this.current_game.team_playing);
});
