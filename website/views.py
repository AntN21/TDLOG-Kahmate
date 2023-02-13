"""
Provides the routing mechanisms
"""
from flask import Blueprint, render_template, request
from controller import Controller
from constants import Teams
from . import SOCKET

views = Blueprint("views", __name__)

controller = Controller(SOCKET)


def render_game(team, current_game):
    """
    Draws the game template with the game json, team (red/blue), player json,
    and player names as the arguments.
    """
    return render_template("game.html", current_game=current_game, client_team=str(team))


def game_view(team, current_request):
    """
    Show a player's perspective. If a post has been made (any button click), it will handle it.
    """
    current_game = controller.current_game
    if current_request.method == "POST":
        if "instructions" in current_request.form:
            return render_template("instructions.html")
        controller.process_game(team, current_request.form)

    return render_game(team, current_game.to_json())


@views.route("/" + str(Teams.RED), methods=["POST", "GET"])
def red():
    """Show red player's perspective"""
    return game_view(Teams.RED, request)


@views.route("/" + str(Teams.BLUE), methods=["POST", "GET"])
def blue():
    """Show blue player's perspective"""
    return game_view(Teams.BLUE, request)


@views.route("/", methods=["POST", "GET"])
def player_selection():
    """
    Initial page routing. It shows the player selection menu
    """
    if request.method == "POST":
        return controller.process_player_selection(request.form)
    return render_template("player_selection.html")
