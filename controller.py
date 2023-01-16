from constants import MOVE, PASS, PLACKAGE, FORCED_PASSAGE, BALL_KICK
import re
from game import Game
from flask import render_template, redirect


class Controller:
    def __init__(self, SOCKET):
        self.current_game = Game()
        self.socket = SOCKET

    def process_player_selection(self, form):
        if "start_game" in form:
            if self.current_game.teams["red"].custom_name == "":
                playe_1_name = form["player_name"]
                self.current_game.set_custom_name("red", playe_1_name)
                self.socket.emit("updateMenu", {"current_game": self.current_game.toJSON()})
                self.socket.emit("updateGameInfo", {"current_game": self.current_game.toJSON()})
                return redirect("/red")
            if self.current_game.teams["blue"].custom_name == "":
                player_2_name = form["player_name"]
                self.current_game.set_custom_name("blue", player_2_name)
                self.socket.emit("updateMenu", {"current_game": self.current_game.toJSON()})
                self.socket.emit("updateGameInfo", {"current_game": self.current_game.toJSON()})
                return redirect("/blue")
        if "instructions" in form:
            return render_template("instructions.html")
        if "back" in form:
            return render_template("player_selection.html")


    def process(self, team, form):
        if "square" in form:
            position = re.sub(r"[() ]", "", form["square"]).split(",")
            self.current_game.select_square(position[1], position[0], team)
        if "card_1" in form:
            self.current_game.select_duel_card(1, team)
            self.socket.emit("updateMenu", {"current_game": self.current_game.toJSON()})
        if "card_2" in form:
            self.current_game.select_duel_card(2, team)
            self.socket.emit("updateMenu", {"current_game": self.current_game.toJSON()})
        if "card_3" in form:
            self.current_game.select_duel_card(3, team)
            self.socket.emit("updateMenu", {"current_game": self.current_game.toJSON()})
        if "card_4" in form:
            self.current_game.select_duel_card(4, team)
            self.socket.emit("updateMenu", {"current_game": self.current_game.toJSON()})
        if "card_5" in form:
            self.current_game.select_duel_card(5, team)
            self.socket.emit("updateMenu", {"current_game": self.current_game.toJSON()})
        if "card_6" in form:
            self.current_game.select_duel_card(6, team)
            self.socket.emit("updateMenu", {"current_game": self.current_game.toJSON()})
        if "next_turn" in form:
            self.current_game.pass_turn(team)
            self.socket.emit("updateMenu", {"current_game": self.current_game.toJSON()})
            self.socket.emit("updateGameInfo", {"current_game": self.current_game.toJSON()})
        if "ball_kick" in form:
            self.current_game.select_action(BALL_KICK, team)
        if "plackage" in form:
            self.current_game.select_action(PLACKAGE, team)
        if "forced_passage" in form:
            self.current_game.select_action(FORCED_PASSAGE, team)
        if "move" in form:
            self.current_game.select_action(MOVE, team)
        if "pass" in form:
            self.current_game.select_action(PASS, team)

        self.socket.emit("updateBoard", {"current_game": self.current_game.toJSON()})
        if self.current_game.duel is not None:
            self.socket.emit("updateMenu", {"current_game": self.current_game.toJSON()})
        if self.current_game.winner is not None:
            self.socket.emit("updateGameInfo", {"current_game": self.current_game.toJSON()})
            self.socket.emit("updateMenu", {"current_game": self.current_game.toJSON()})
