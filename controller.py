"""
Controller file
"""
import re
from flask import render_template, redirect
from enum import Enum
from constants import Actions, Teams, other
from game import Game

class Instruction(Enum):
    SQUARE = 0
    CARD = 1
    NEXT_TURN = 2
    BALL_KICK = 3
    TACKLE = 4
    FORCED_PASSAGE = 5
    MOVE = 6
    PASS = 7

class Controller:
    """
    From a flask socket_io, the controller class creates a Game and can be modified from the
    view using their forms and executing all updates with the socket
    """

    def __init__(self, socket):
        self.current_game = Game()
        self.socket = socket

    def emit_update_game(self, team):
        """
        Emits the updates game instruction through the socket to all teams
        """
        self.socket.emit(
            "updateGame",
            {"current_game": self.current_game.to_json(), "client_team": Teams.RED.other(team).value},
        )

    def process_player_selection(self, form):
        """
        This method will handle the player selection form events
        """
        if "start_game" in form:
            if self.current_game.teams[Teams.RED].custom_name == "":
                player_1_name = form["player_name"]
                self.current_game.set_custom_name(Teams.RED, player_1_name)
                self.emit_update_game(Teams.RED)
                return redirect("/" + str(Teams.RED))
            if self.current_game.teams[Teams.BLUE].custom_name == "":
                player_2_name = form["player_name"]
                self.current_game.set_custom_name(Teams.BLUE, player_2_name)
                self.emit_update_game(Teams.BLUE)
                return redirect("/" + str(Teams.BLUE))
        if "instructions" in form:
            return render_template("instructions.html")
        return render_template("player_selection.html")

    def process_game(self, team, form):
        """
        This method will handle all game events from the view's form
        """

        print("t  ", team.value)
        print("f",form)
        #team = Teams.RED if team == 'red' else Teams.BLUE
        if "square" in form:
            position = re.sub(r"[() ]", "", form["square"]).split(",")
            self.current_game.select_square(position[1], position[0], team)
        if any("card" in element for element in form):
            card = list(form)[0].split("_")[1]
            self.current_game.select_duel_card(int(card), team)
        if "next_turn" in form:
            self.current_game.pass_turn(team)
        if "ball_kick" in form:
            self.current_game.select_action(Actions.BALL_KICK.value, team)
        if "tackle" in form:
            self.current_game.select_action(Actions.TACKLE.value, team)
        if "forced_passage" in form:
            self.current_game.select_action(Actions.FORCED_PASSAGE.value, team)
        if "move" in form:
            self.current_game.select_action(Actions.MOVE.value, team)
        if "pass" in form:
            self.current_game.select_action(Actions.PASS.value, team)

        self.emit_update_game(team)
