"""
Game contains all game information, it also handles the main functions needed
to play the game.
"""
import json
import random as rd
from math import floor
from enum import Enum
from constants import Teams
from board import Board
from players.rugby_player import RugbyPlayer
from players.ordinary import Ordinary
from players.clever import Clever
from players.fast import Fast
from players.strong import Strong
from players.tough import Tough
from actions.action_manager import ActionManager


class Team:
    """
    The class team contains the name of the team (red or blue, from the constants file)
    the custom name of the player, the cards that they have and the quantity of players moved.
    """

    def __init__(self, name, custom_name=""):
        self._name = name
        self.players_moved = []
        self.custom_name = custom_name
        self.cards = list(range(1, 6 + 1))

    def to_dict(self):
        """
        This function converts the class to a dict.
        """
        team_json = {}
        team_json["custom_name"] = self.custom_name
        team_json["players_moved"] = [str(player) for player in self.players_moved]
        team_json["cards"] = self.cards
        return team_json



class Game:
    """
    The Game class will contain all the information related with the state of the game. This
    will be the board, the turn that we are currently on, the selected case, the selected action,
    if there is any winner, if there is a duel currently taking place, both teams information, and
    the action_manager that will handle all possible moves.
    """

    def __init__(self):
        self._board = Board()
        self._turn = 0
        self._selected_case = None
        self._selected_action = None
        self._winner = None
        self.initial_placing()
        self._duel = None
        self.teams = {
            Teams.RED: Team(Teams.RED),
            Teams.BLUE: Team(Teams.BLUE),
        }
        self.team_playing = Teams.RED
        self._action_class = ActionManager(self._board.width, self._board.height)
        self._action_class.update(self)

    @property
    def selected_case(self):
        return self._selected_case

    @property
    def duel(self):
        return self._duel

    @property
    def winner(self):
        return self._winner

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, n_board):
        self._board = n_board

    def initial_placing(self):
        """Place the players in an initial configuration"""
        height = 1
        for player in [
            Ordinary(Teams.RED),
            Strong(Teams.RED),
            Tough(Teams.RED),
            Fast(Teams.RED),
            Clever(Teams.RED),
            Ordinary(Teams.RED),
        ]:
            self._board.put_player(player, 1, height)
            height += 1
        height = 1
        for player in [
            Ordinary(Teams.BLUE),
            Strong(Teams.BLUE),
            Tough(Teams.BLUE),
            Fast(Teams.BLUE),
            Clever(Teams.BLUE),
            Ordinary(Teams.BLUE),
        ]:
            self._board.put_player(player, self.board.width - 2, height)
            height += 1
        self._board.put_ball(
            floor(self.board.width / 2), rd.randint(1, self.board.height - 2)
        )

    def set_custom_name(self, team, custom_name):
        """Sets the custom name (nickname) of one team"""
        self.teams[team].custom_name = custom_name

    def select_square(self, pos_x, pos_y, team):
        """
        Selects a square. If a player and an action are already selected it executes the action,
        if not, it can select a player or diselect the old one.
        This method updates the selected case (marked with red)
        """
        if team != self.team_playing or self.duel is not None:
            return
        self.board.clear_selected()
        selected_case = self.board.square(int(pos_x), int(pos_y))
        if self.selected_case is not None:
            if selected_case.available:
                result = None
                for possible_actions in self._action_class.possible_moves[
                    self._selected_action
                ][self.selected_case.pos_y][self.selected_case.pos_x]:
                    if (
                        possible_actions.position2[0] == selected_case.pos_x
                        and possible_actions.position2[1] == selected_case.pos_y
                    ):
                        result = possible_actions.play(self)

                if isinstance(result, Board):
                    self._board = result
                    goal = (
                        self.board.width - 1
                        if self.team_playing == Teams.RED
                        else 0
                    )
                    if selected_case.pos_x == goal:
                        self._winner = self.team_playing
                else:
                    self._duel = result
                self._action_class.update(self)
            self._selected_case = None
            self.board.clear_selected()
        else:
            if selected_case.player is not None and selected_case.player.team == team:
                self.board.square(
                    selected_case.pos_x, selected_case.pos_y
                ).set_selected(True)
                self._selected_case = selected_case
        self.board.clear_available()

    def select_action(self, action, team):
        """
        Selects the action that the current team playing takes. Updates the board
        accordingly showing all available squares.
        """
        if (
            team != self.team_playing
            or self._selected_case is None
            or self._selected_case.player is None
            or self.duel is not None
        ):
            return
        self._selected_action = action
        self.board.clear_available()
        for initial_line in self._action_class.possible_moves[action]:
            for initial_square in initial_line:
                for possible_action in initial_square:
                    if (
                        possible_action.position1[0] == self.selected_case.pos_x
                        and possible_action.position1[1] == self.selected_case.pos_y
                    ):
                        self.board.square(
                            possible_action.position2[0], possible_action.position2[1]
                        ).set_available(True)

    def select_duel_card(self, card, team):
        """
        Selects the team's card for a duel, if both players have already selected a card
        it should resolve the duel and resume the game.
        """
        self.duel.choose_card(self, card, team)
        if self.duel.is_ready():
            result = None
            for possible_actions in self._action_class.possible_moves[
                self._selected_action
            ][self.duel.position1[1]][self.duel.position1[0]]:
                if (
                    possible_actions.position2[0] == self.duel.position2[0]
                    and possible_actions.position2[1] == self.duel.position2[1]
                ):
                    result = possible_actions.play(self)
            if isinstance(result, Board):
                self._board = result
                self._duel = None
                self._action_class.update(self)
            else:
                self._duel = result
        return

    def pass_turn(self, team):
        """Finishes a player's turn"""

        if team != self.team_playing:
            return
        if self._winner is not None:
            return
        self._turn += 1

        self._selected_case = None
        self.board.clear_available()
        self.board.clear_selected()
        self.team_playing = Teams.RED.other(self.team_playing)
        self.teams[self.team_playing].players_moved = []
        for square in self.board.squares:
            if square.player is not None:
                square.player.reset_moves()
                if square.player.team == self.team_playing:
                    square.player.recover()
        self._action_class.update(self)

    def to_json(self):
        """
        Converts the game state into a json to be used in the java script file
        """
        res = {}
        res["team_playing"] = self.team_playing.value
        res["board"] = []
        for square in self.board.squares:
            res["board"].append(
                {
                    "player": -1 if square.player is None else 100 * square.player.stunned_state
                                                            + 10 * square.player.type.value + square.player.team.value,
                    "player_string": None if square.player is None else str(square.player),
                    "ball": square.ball,
                    "available": square.available,
                    "selected": square.selected,
                }
            )

        if self.selected_case is not None:
            selected_case = {}
            selected_case["position"] = [
                self.selected_case.pos_x,
                self.selected_case.pos_y,
            ]
            selected_case["movements_left"] = self.selected_case.player.available_moves
            res["selected_case"] = selected_case
        else:
            res["selected_case"] = None

        res["actions"] = self._action_class.get_possible_moves()

        team_red = self.teams[Teams.RED].to_dict()
        team_blue = self.teams[Teams.BLUE].to_dict()

        res["team_red"] = team_red
        res["team_blue"] = team_blue

        if self.duel is not None:
            duel = {}
            duel["team_1_cards"] = self.teams[Teams.RED].cards
            duel["team_2_cards"] = self.teams[Teams.BLUE].cards
            duel["team_1_fighter"] = str(
                self.board.square(
                    self._duel.position1[0], self._duel.position1[1]
                ).player
            )
            duel["team_2_fighter"] = str(
                self.board.square(
                    self._duel.position2[0], self._duel.position2[1]
                ).player
            )
            res["duel"] = duel
        else:
            res["duel"] = None

        if self.winner is not None:
            res["winner"] = str(self.team_playing)
        else:
            res["winner"] = None

        jres = json.dumps(res)
        jsonFile = open("test.json", "w")
        jsonFile.write(jres)
        jsonFile.close()

        return json.dumps(res)

    def load_json(self, json_file):
        RUGBYPLAYERS = [Ordinary, Clever, Strong, Tough, Fast]
        """
        Loads a game state from a json file
        """
        game_state = json.loads(json_file.read())
        self.team_playing = game_state["team_playing"]
        self.board = Board()
        for index in range(len(game_state["board" ])):

            self.board.squares[index].set_ball(game_state["board"][index]["ball"])
            player_data = game_state["board"][index]["player"]
            stunned_state = player_data/100
            player_type = (player_data - 100*stunned_state ) / 10
            team_index = player_data % 10
            player = None if team_index == -1 else RUGBYPLAYERS[player_type](list(Teams)[team_index])
            player.stunned_state = stunned_state

            team_strings = ["team_red", "team_blue"]
            for index in range(2):
                team = self.teams[list(Teams)[index]]
                team.custom_name = game_state[team_strings[index]]["custom_name"]
                team.players_moved = game_state[team_strings[index]]["custom_name"]
                team.cards = game_state[team_strings[index]]["cards"]
