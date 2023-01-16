"""
Provides the routing mechanisms
"""
from controller import Controller
from flask import Blueprint, render_template, redirect, request
from . import SOCKET

views = Blueprint("views", __name__)
chips = [["" for x in range(11)] for y in range(8)]

controller = Controller(SOCKET)


def render_game(team, current_game):
    """
    Draws the game template with the game json, team (red/blue), player json,
    and player names as the arguments.
    """

    return render_template(
        "game.html",
        current_game = current_game,
        client_team = team
    )


def game_view(team, request):
    """
    Show a player's perspective. If a post has been made (any button click), it will handle it.
    """
    current_game = controller.current_game
    if request.method == "POST":
        if "instructions" in request.form:
            return render_template("instructions.html")
        controller.process(team, request.form)

    return render_game(team, current_game.toJSON())


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
        return controller.process_player_selection(request.form)
    return render_template("player_selection.html")
