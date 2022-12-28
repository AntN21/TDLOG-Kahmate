var socket = io.connect()
var players = ["clever_red", "strong_red", "tough_red", "fast_red", "ordinary_red", "ko_red",
                "clever_blue", "strong_blue", "tough_blue", "fast_blue", "ordinary_blue","ko_blue"];

function get_src(player) {
    return "../static/images/" + player + ".png";
}

function updateBoard(board) {
    for (let row = 0; row < board._height; row++) {
        for (let col = 0; col < board._width; col++) {
            var selected_square_element = document.getElementById('('+String(row)+', '+String(col) + ')')
            var selected_square_json = board._squares[row * board._width + col]
            var child = selected_square_element.lastElementChild; 
            while (child) {
                selected_square_element.removeChild(child);
                child = selected_square_element.lastElementChild;
            }
            if(selected_square_json._ball) {
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
            if(selected_square_json._player) {
                var image = document.createElement("img");
                var player_type = selected_square_json._player._type
                var player_team = selected_square_json._player._team
                image.src = get_src(player_type+"_"+player_team);
                image.draggable = false;
                image.style.width = "40px";
                image.style.width = "40px";
                selected_square_element.appendChild(image);
            }
            if(selected_square_json._available || selected_square_json._selected) {
                if(selected_square_json._available)
                    selected_square_element.style.borderColor = "white"
                if(selected_square_json._selected){
                    selected_square_element.style.borderColor = "red"
                }
            } else {
                selected_square_element.style.borderColor = "black"
            }
        }
    }
}

function updateMessage(message) {

}

function clearMenu() {
    document.getElementById("move").style.display = "None";
    document.getElementById("ball_kick").style.display = "None";
    document.getElementById("plackage").style.display = "None";
    document.getElementById("forced_passage").style.display = "None";
    document.getElementById("pass").style.display = "None";
    document.getElementById("next_turn").style.display = "None";
}

function updateMenu(current_game, player) {
    console.log(current_game)
    document.getElementById("turn_card").style.backgroundColor = current_game.team_playing;
    document.getElementById("turn_text").innerHTML = "It is " + current_game.team_playing + "'s turn";
    clearMenu()
    if(current_game.team_playing == player.team) {
        document.getElementById("next_turn").style.display = "inline";
        if(current_game._selected_case._player._available_moves > 0) {
            document.getElementById("move").style.display = "inline";
        }
        if(current_game._selected_case._ball) {
            document.getElementById("pass").style.display = "inline";
            document.getElementById("ball_kick").style.display = "inline";
            // Check if an opponent is next to the selected_case and there is an available square
            if(current_game._selected_case.x)
            document.getElementById("forced_passage").style.display = "inline";
        }
        if(!current_game._selected_case._ball) {
            document.getElementById("plackage").style.display = "inline";
        }
        if(current_game.possible_interception) {
            //set interception true
        }
        if(current_game._duel) {

        }
    }
    //if(current_game._selected_case._player)
}

function updatePlayerInfo(player) {
    document.getElementById("player_info_card").style.backgroundColor = player.team;
}

function updateGame(current_game, player) {
    updateBoard(current_game._board)
    updateMessage(current_game._message)
    updatePlayerInfo(player)
    updateMenu(current_game, player)
}

socket.on("updateBoard", function (data) {
    this.current_game = JSON.parse(data.current_game);
    updateBoard(this.current_game._board);
});

socket.on("updateMenu", function (data) {
    this.current_game = JSON.parse(data.current_game);
    updateMenu(this.current_game, this.current_game.team_playing);
});