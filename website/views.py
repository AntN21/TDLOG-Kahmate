"""
Provides the routing mechanisms
"""
import re
import json
import random
from constants import MOVE, PASS, PLACKAGE, FORCED_PASSAGE, BALL_KICK
from flask import Blueprint, render_template, redirect, request
import game
from game import Ordinary

from . import socket

views = Blueprint("views", __name__)
chips = [["" for x in range(11)] for y in range(8)]
current_game = game.Game()


PLAYER_NAME_1 = ""
PLAYER_NAME_2 = ""
cards_1 = [1, 2, 3, 4, 5, 6]
cards_2 = [1, 2, 3, 4, 5, 6]

blue_chips = [
    "clever_blue",
    "ordinary_blue",
    "fast_blue",
    "strong_blue",
    "tough_blue",
    "ko_blue",
]
red_chips = [
    "clever_red",
    "ordinary_red",
    "fast_red",
    "strong_red",
    "tough_red",
    "ko_red",
]

def player_json(player):
    return json.loads("{\"team\": \"" + player + "\"}")

def render_game(player):
    return render_template(
        "game.html",
        current_game = current_game.to_json(),
        player_name = player,
        player_json = player_json(player),
        player_cards = current_game.teams[player],
        player_name_1=PLAYER_NAME_1,
        player_name_2=PLAYER_NAME_2,
    )


def game_view(player, option_chips, request):
    if request.method == "POST":
        if "next" in request.form:
            position = re.sub(r"[() ]", "", request.form["next"]).split(",")
            current_game.select_square(position[1], position[0], player)
        if "instructions" in request.form:
            return render_template("instructions.html")
        if "back" in request.form:
            render_game(player)
        if "next_turn" in request.form:
            if current_game.team_playing == player:
                current_game.pass_turn()
                socket.emit("updateMenu", {"current_game": current_game.to_json()})
        if "ball_kick" in request.form:
            current_game.select_action(BALL_KICK, player)
        if "plackage" in request.form:
            current_game.select_action(PLACKAGE, player)
        if "forced_passage" in request.form:
            current_game.select_action(FORCED_PASSAGE, player)
        if "move" in request.form:
            current_game.select_action(MOVE, player)
        if "pass" in request.form:
            current_game.select_action(PASS, player)

        socket.emit("updateBoard", {"current_game": current_game.to_json()})

    return render_game(player)


@views.route("/red", methods=["POST", "GET"])
def red():
    return game_view("red", blue_chips, request)


@views.route("/blue", methods=["POST", "GET"])
def blue():
    return game_view("blue", red_chips, request)


@views.route("/", methods=["POST", "GET"])
def player_selection():
    if request.method == "POST":
        if "start_game" in request.form:
            global PLAYER_NAME_1, PLAYER_NAME_2
            if PLAYER_NAME_1 == "":
                PLAYER_NAME_1 = request.form["player_name"]
                return redirect("/red")
            if PLAYER_NAME_2 == "":
                PLAYER_NAME_2 = request.form["player_name"]
                return redirect("/blue")
        if "instructions" in request.form:
            return render_template("instructions.html")
        if "back" in request.form:
            return render_template("player_selection.html")
    return render_template("player_selection.html")
