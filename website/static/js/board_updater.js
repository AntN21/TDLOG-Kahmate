var socket = io.connect()

const Teams = {
    RED: "red",
    BLUE: "blue"
}

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
    document.getElementById("tackle").style.display = "None";
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
    if(current_game.winner != null){
        document.getElementById("turn_text").innerHTML = "PLAYER " + current_game.winner + " WON!";
        clearMenu()
        return
    } else {
        document.getElementById("turn_text").innerHTML = "It is " + current_game.team_playing + "'s turn";
    }
    clearMenu()
    if(current_game.team_playing == client_team) {
        document.getElementById("next_turn").style.display = "inline";
        var selected_case = current_game.selected_case;
        if(selected_case != null) {
            for(i in current_game.actions) {

                action = current_game.actions[i]
                if(action.position_1[0] == selected_case.position[0] &&
                    action.position_1[1] == selected_case.position[1]) {
                    if(action.type == "Move")
                        document.getElementById("move").style.display = "inline";
                    if(action.type == "ForcedPassage")
                        document.getElementById("forced_passage").style.display = "inline";
                    if(action.type == "Pass")
                        document.getElementById("pass").style.display = "inline";
                    if(action.type == "BallKick")
                        document.getElementById("ball_kick").style.display = "inline";
                    if(action.type == "Tackle")
                       document.getElementById("tackle").style.display = "inline";
                }
            }
        }
    }

    if(current_game.duel != null) {
        document.getElementById("duel_menu").style.display = "flex";
        document.getElementById("duel_info").innerHTML = current_game.duel.team_1_fighter + " vs " + current_game.duel.team_2_fighter
        clearMenu();
        var cards = client_team == Teams.RED ? 
                    current_game.team_red.cards :
                    current_game.team_blue.cards;
        for(let i = 0; i < cards.length; i++) {
            document.getElementById("card_" + cards[i]).style.display = "inline";
        }
    } else {
        document.getElementById("duel_menu").style.display = "None";
    }
}

function updateGameInfo(current_game, client_team) {
    /**
     *   Updates all game info shown (current player's turn, available moves, available cards)
     */
    document.getElementById("player_info_card").style.backgroundColor = client_team;
    document.getElementById("player_red_custom_name").innerHTML = current_game.team_red.custom_name;
    document.getElementById("player_blue_custom_name").innerHTML = current_game.team_blue.custom_name;
    var team = client_team == Teams.RED ? current_game.team_red : current_game.team_blue; 
    if(current_game.selected_case != null && client_team == current_game.team_playing){
        document.getElementById("player_moves_left").innerHTML = "Player moves left: " + current_game.selected_case.movements_left;
    } else {
        document.getElementById("player_moves_left").innerHTML = "";
    }
    document.getElementById("team_moves_left").innerHTML = "Team moves left: " + (2-team.players_moved.length);
    document.getElementById("cards_left").innerHTML = "Team cards left: " + team.cards;
}

function updateGame(current_game, team) {
    console.log(current_game)
    this.current_game = JSON.parse(current_game);
    updateBoard(this.current_game.board)
    updateGameInfo(this.current_game, team)
    updateMenu(this.current_game, team)
    document.getElementById("all").style.display = "flex";
}

socket.on("updateGame", function (data) {
    this.current_game = JSON.parse(data.current_game);
    updateBoard(this.current_game.board);
    updateMenu(this.current_game, data.client_team);
    updateGameInfo(this.current_game, data.client_team);
});
