from flask import Blueprint, render_template, redirect, request
import re
import random

from . import socket

views = Blueprint("views", __name__)
chips = [["" for x in range(11)] for y in range(8)]

player_name_1 = ""
player_name_2 = ""
cards_1 = [1,2,3,4,5,6]
cards_2 = [1,2,3,4,5,6]
movements_done_1 = 0
movements_done_2 = 0
movements_left_1 = 0
movements_left_2 = 0

blue_chips = ["clever_blue", "ordinary_blue", "fast_blue", "strong_blue", "tough_blue", "ko_blue"]
red_chips = ["clever_red", "ordinary_red", "fast_red", "strong_red", "tough_red", "ko_red"]

def render_game(player):
    return render_template("game.html", chips=chips, player=player,
                player_name_1=player_name_1, player_name_2=player_name_2)

def game(player, option_chips, request):
    if request.method == "POST":
        if("next" in request.form):
            position = re.sub(r"[() ]", "", request.form["next"]).split(",")
            chips[int(position[0])][int(position[1])] = random.choice(option_chips)
            if random.randint(0, 2) == 1:
                chips[int(position[0])][int(position[1])] += "ball"
            socket.emit("updateChips", {'chips': chips})
        if("instructions" in request.form):
            return render_template("instructions.html")
        if("back" in request.form):
            render_game(player)
    return render_game(player)

@views.route("/player_1", methods=["POST", "GET"])
def player_1():
    return game("player_1", blue_chips, request)

@views.route("/player_2", methods=["POST", "GET"])
def player_2():
    return game("player_2", red_chips, request)

@views.route("/", methods=["POST", "GET"])
def player_selection():
    if request.method == "POST":
        if("start_game" in request.form):
            global player_name_1, player_name_2
            if player_name_1 == "":
                player_name_1 = request.form["player_name"]
                return redirect('/player_1')
            elif player_name_2 == "":
                player_name_2 = request.form["player_name"]
                return redirect('/player_2')
        if("instructions" in request.form):
            return render_template("instructions.html")
        if("back" in request.form):
            return render_template("player_selection.html")
    return render_template("player_selection.html")
