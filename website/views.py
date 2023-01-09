"""
Provides the routing mechanisms
"""
import re
import json
from flask import Blueprint, render_template, redirect, request
from constants import MOVE, PASS, PLACKAGE, FORCED_PASSAGE, BALL_KICK
import game
from . import SOCKET

views = Blueprint("views", __name__)
chips = [["" for x in range(11)] for y in range(8)]
current_game = game.Game()


PLAYER_NAME_1 = ""
PLAYER_NAME_2 = ""

def player_json(team):
    return json.loads("{\"team\": \"" + team + "\"}")

def render_game(team):
    """
    Draws the game template with the game json, team (red/blue), player json,
    and player names as the arguments.
    """

    return render_template(
        "game.html",
        current_game = current_game.toJSON(),
        team = team,
        player_json = player_json(team),
        player_name_1=PLAYER_NAME_1,
        player_name_2=PLAYER_NAME_2,
    )


def game_view(team, request):
    """
    Show a player's perspective. If a post has been made (any button click), it will handle it.
    """
    if request.method == "POST":
        if "square" in request.form:
            position = re.sub(r"[() ]", "", request.form["square"]).split(",")
            current_game.select_square(position[1], position[0], team)
        if "card_1" in request.form:
            current_game.select_duel_card(1, team)
        if "card_2" in request.form:
            current_game.select_duel_card(2, team)
        if "card_3" in request.form:
            current_game.select_duel_card(3, team)
        if "card_4" in request.form:
            current_game.select_duel_card(4, team)
        if "card_5" in request.form:
            current_game.select_duel_card(5, team)
        if "card_6" in request.form:
            current_game.select_duel_card(6, team)
        if "instructions" in request.form:
            return render_template("instructions.html")
        if "back" in request.form:
            render_game(team)
        if "next_turn" in request.form:
            if current_game.team_playing == team:
                current_game.pass_turn()
                SOCKET.emit("updateMenu", {"current_game": current_game.toJSON()})
        if "ball_kick" in request.form:
            current_game.select_action(BALL_KICK, team)
        if "plackage" in request.form:
            current_game.select_action(PLACKAGE, team)
        if "forced_passage" in request.form:
            current_game.select_action(FORCED_PASSAGE, team)
        if "move" in request.form:
            current_game.select_action(MOVE, team)
        if "pass" in request.form:
            current_game.select_action(PASS, team)

        SOCKET.emit("updateBoard", {"current_game": current_game.toJSON()})

    return render_game(team)


@views.route("/red", methods=["POST", "GET"])
def red():
    """Show red player's perspective"""
    return game_view("red", request)


@views.route("/blue", methods=["POST", "GET"])
def blue():
    """Show blue player's perspective"""
    return game_view("blue", request)


@views.route("/", methods=["POST", "GET"])
def player_selection():
    """
    Initial page routing. It shows the player selection menu
    """

    if request.method == "POST":
        if "start_game" in request.form:
            global PLAYER_NAME_1, PLAYER_NAME_2
            if PLAYER_NAME_1 == "":
                PLAYER_NAME_1 = request.form["player_name"]
                current_game.set_custom_name("red", PLAYER_NAME_1)
                SOCKET.emit("updateMenu", {"current_game": current_game.toJSON()})
                return redirect("/red")
            if PLAYER_NAME_2 == "":
                PLAYER_NAME_2 = request.form["player_name"]
                current_game.set_custom_name("blue", PLAYER_NAME_2)
                SOCKET.emit("updateMenu", {"current_game": current_game.toJSON()})
                return redirect("/blue")
        if "instructions" in request.form:
            return render_template("instructions.html")
        if "back" in request.form:
            return render_template("player_selection.html")
    return render_template("player_selection.html")
