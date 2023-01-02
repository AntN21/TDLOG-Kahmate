"""
    game contains all game information, it also handles the main functions needed
    to play the game.
"""
import json
from constants import MOVE, FORCED_PASSAGE, BALL_KICK, PASS, PLACKAGE , BLUE_TEAM, RED_TEAM
from board import Board
from players.ordinary import Ordinary
from players.clever import Clever
from players.fast import Fast
from players.strong import Strong
from players.tough import Tough
from actions import accessibles_cases, execute_action

class Team:
    def __init__(self, name):
        self._name = name
        self.Cards = list(range(1, 6 + 1))

class Game:
    def __init__(self):
        self._board = Board()
        self._turn = 0 
        self._message = "Starts"
        self._selected_case = None
        self._selected_action = "starting"
        self._red_players = [Ordinary(RED_TEAM), Ordinary(RED_TEAM), Strong(RED_TEAM),
                   Tough(RED_TEAM), Fast(RED_TEAM), Clever(RED_TEAM)]
        self._blue_players = [Ordinary(BLUE_TEAM), Ordinary(BLUE_TEAM), Strong(BLUE_TEAM),
                   Tough(BLUE_TEAM), Fast(BLUE_TEAM), Clever(BLUE_TEAM)]
        self.initial_placing()
        self._started = False
        self._duel = False
        self._duel_player_1 = None
        self._duel_player_2 = None
        self.teams = {RED_TEAM: Team(RED_TEAM), BLUE_TEAM: Team(BLUE_TEAM)}
        self.team_playing = RED_TEAM

    @property
    def turn(self):
        return self._turn

    @property
    def message(self):
        return self._message

    @property
    def selected_case(self):
        return self._selected_case

    @property
    def duel(self):
        return self._duel

    @property
    def duel_palayer_1(self):
        return self._duel_player_1

    @property
    def duel_palayer_2(self):
        return self._duel_player_2

    @property
    def board(self):
        return self._board

    def initial_placing(self):
        """Place the players in an initial configuration"""
        height = 1
        for player in self._red_players:
            self._board.put_player(player, 4, height)
            height += 1
        height = 1
        for player in self._blue_players:
            self._board.put_player(player, 6, height)
            height += 1

    def get_availables(self):
        """
            This method should return all the available squares when a player and an
            action are selected.
        """
        availables = []
        if self._selected_action == MOVE:
            if not self._started:
                cols = (0, 1) if self.team_playing==RED_TEAM else (9, 10)
                for row in range(self.board.height):
                    for col in cols:
                        availables.append((col, row))
            if self._started:
                availables = accessibles_cases(self.selected_case.player.available_moves,
                                               self.team_playing,
                                               self.board,
                                               self.selected_case.get_position())
        return availables

    def select_square(self, x, y, team):
        """
            Selects a square. If a player and an action are already selected it executes the action,
            if not, it can select a player or diselect the old one.
            This method updates the selected case (marked with red)
        """
        if team != self.team_playing:
            return
        self.board.clear_selected()
        selected_case = self.board.square(int(x), int(y))
        if self.selected_case is not None:
            if selected_case.available:
                duel, selected_case, self._selected_case = execute_action(self._started,
                                                                          self.selected_case,
                                                                          selected_case,
                                                                          self._selected_action)
                if duel:
                    self._duel_player_1 = self.selected_case.player
                    self._duel_player_2 = selected_case.player
                    self._duel = True
            self._selected_case = None
            self.board.clear_selected()
        else:
            if selected_case.player is not None and selected_case.player.team == team:
                self.board.square(selected_case.x, selected_case.y).set_selected(True)
                self._selected_case = selected_case
        self.board.clear_available()

    def select_action(self, action, team):
        """
            Selects the action that the current team playing takes. Updates the board
            accordingly showing all available squares.
        """
        if team != self.team_playing or self._selected_case is None or self._selected_case.player is None:
            return
        self._selected_action = action
        self.board.clear_available()
        availables = self.get_availables()
        for available in availables:
            self.board.square(available[0], available[1]).set_available(True)

    def pass_turn(self):
        """ Finishes a player's turn """
        self._turn += 1
        if self._turn > 1:
            self._started = True
        for player in self._red_players:
            player.full_reset()
        for player in self._blue_players:
            player.full_reset()
        self._selected_case = None
        self.board.clear_available()
        self.board.clear_selected()
        self.team_playing = BLUE_TEAM if self.team_playing == RED_TEAM else RED_TEAM

    def to_json(self):
        """ Converts game to JSON """
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)
