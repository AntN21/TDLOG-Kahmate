"""
    game contains all game information, it also handles the main functions needed
    to play the game.
"""
import json
import random as rd
from constants import MOVE, FORCED_PASSAGE, BALL_KICK, PASS, PLACKAGE , BLUE_TEAM, RED_TEAM
from board import Board
from players.ordinary import Ordinary
from players.clever import Clever
from players.fast import Fast
from players.strong import Strong
from players.tough import Tough
from actions import Actions

class Team:

    def __init__(self, name, custom_name = ""):
        self._name = name
        self.players_moved = []
        self.custom_name = custom_name
        self.cards = list(range(1, 6 + 1))

    def to_dict(self):
        team_json = {}
        team_json["custom_name"] = self.custom_name
        team_json["players_moved"] = [str(player) for player in self.players_moved]
        team_json["cards"] = self.cards
        return team_json

class Game:
    def __init__(self):
        self._board = Board()
        self._turn = 0
        self._selected_case = None
        self._selected_action = "starting"
        self._winner = None
        self.initial_placing()
        self._started = False
        self._duel = None
        self.teams = {RED_TEAM: Team(RED_TEAM), BLUE_TEAM: Team(BLUE_TEAM)}
        self.team_playing = RED_TEAM
        self._action_class = Actions(self._board.width, self._board.height)
        self._action_class.update(self)

    @property
    def turn(self):
        return self._turn

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

    def initial_placing(self):
        """Place the players in an initial configuration"""
        height = 0
        for player in [Ordinary(RED_TEAM), Ordinary(RED_TEAM), Strong(RED_TEAM),
                   Tough(RED_TEAM), Fast(RED_TEAM), Clever(RED_TEAM)]:
            self._board.put_player(player, 1, height)
            height += 1
        height = 0
        for player in [Ordinary(BLUE_TEAM), Ordinary(BLUE_TEAM), Strong(BLUE_TEAM),
                   Tough(BLUE_TEAM), Fast(BLUE_TEAM), Clever(BLUE_TEAM)]:
            self._board.put_player(player, 11, height)
            height += 1
        self._board.put_ball(6,rd.randint(1,6))

    def set_custom_name(self, team, custom_name):
        self.teams[team].custom_name = custom_name

    def select_square(self, x, y, team):
        """
            Selects a square. If a player and an action are already selected it executes the action,
            if not, it can select a player or diselect the old one.
            This method updates the selected case (marked with red)
        """
        if team != self.team_playing or self.duel is not None:
            return
        self.board.clear_selected()
        selected_case = self.board.square(int(x), int(y))
        if self.selected_case is not None:
            if selected_case.available:
                result = None
                for possible_actions in self._action_class.possible_moves[self._selected_action][self.selected_case.y][self.selected_case.x]:
                    if possible_actions.position2[0] == selected_case.x and possible_actions.position2[1] == selected_case.y:
                        result = possible_actions.play(self)
                    #if possible_action.position1[0] == self.selected_case.x and possible_action.position1[1] == self.selected_case.y:
                    #    self.board.square(possible_action.position2[0], possible_action.position2[1]).set_available(True)

                if isinstance(result, Board):
                    self._board = result
                    goal = 12 if self.team_playing == "red" else 0
                    if selected_case.x == goal:
                        self._winner = self.team_playing
                else:
                    self._duel = result
                self._action_class.update(self)
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
        if team != self.team_playing or self._selected_case is None or self._selected_case.player is None or self.duel is not None:
            return
        self._selected_action = action
        self.board.clear_available()
        for initial_line in self._action_class.possible_moves[action]:
            for initial_square in initial_line:
                for possible_action in initial_square:
                    if possible_action.position1[0] == self.selected_case.x and possible_action.position1[1] == self.selected_case.y:
                        self.board.square(possible_action.position2[0], possible_action.position2[1]).set_available(True)


    def select_duel_card(self, card, team):
        """
            Selects the team's card for a duel, if both players have already selected a card
            it should resolve the duel and resume the game.
        """
        self.duel.choose_card(self, card, team)
        if self.duel.is_ready():
            result = None
            for possible_actions in self._action_class.possible_moves[self._selected_action][self.duel.position1[1]][self.duel.position1[0]]:
                if possible_actions.position2[0] == self.duel.position2[0] and possible_actions.position2[1] == self.duel.position2[1]:
                    result = possible_actions.play(self)
            if isinstance(result, Board):
                self._board = result
                self._duel = None
                if self._selected_action == PLACKAGE:
                    self.pass_turn(self.team_playing)
                else:
                    self._action_class.update(self)
            else:
                self._duel = result
        return

    def pass_turn(self, team):
        """ Finishes a player's turn """

        if team != self.team_playing:
            return
        if self._winner is not None:
            return
        self._turn += 1
        if self._turn > 1:
            self._started = True

        self._selected_case = None
        self.board.clear_available()
        self.board.clear_selected()
        self.team_playing = BLUE_TEAM if self.team_playing == RED_TEAM else RED_TEAM
        self.teams[self.team_playing].players_moved = []
        for square in self.board.squares:
            if square.player is not None:
                square.player.reset_moves()
                if square.player.team == self.team_playing:
                    square.player.recover()
        self._action_class.update(self)

    def toJSON(self):
        res={}
        res['team_playing']=self.team_playing
        res['board']=[]
        for square in self.board.squares:
            res['board'].append({'player': None if square.player is None else str(square.player),
                                'ball':square.ball,
                                'available':square.available,
                                'selected':square.selected})
        
        if self.selected_case is not None:
            selected_case = {}
            selected_case["position"] = [self.selected_case.x, self.selected_case.y]
            selected_case["movements_left"] = self.selected_case.player.available_moves
            res["selected_case"] = selected_case
        else:
            res["selected_case"] = None

        possible_moves = []
        for action_type  in self._action_class.possible_moves:
            for initial_line in self._action_class.possible_moves[action_type]:
                for initial_square in initial_line:
                    for possible_action in initial_square:
                        action_json = {}
                        action_json['type'] = action_type
                        action_json['position_1'] = possible_action.position1
                        action_json['position_2'] = possible_action.position2
                        possible_moves.append(action_json)
        res['actions'] = possible_moves


        team_red = self.teams['red'].to_dict()
        team_blue = self.teams['blue'].to_dict()

        res["team_red"] = team_red
        res["team_blue"] = team_blue

        if self.duel is not None:
            duel = {}
            duel['team_1_cards'] = self.teams[RED_TEAM].cards
            duel['team_2_cards'] = self.teams[BLUE_TEAM].cards
            duel['team_1_fighter'] = str(self.board.square(self._duel.position1[0], self._duel.position1[1]).player)
            duel['team_2_fighter'] = str(self.board.square(self._duel.position2[0], self._duel.position2[1]).player)
            res['duel'] = duel
        else:
            res['duel'] = None

        if self.winner is not None:
            res['winner'] = self.team_playing
        else:
            res['winner'] = None

        return json.dumps(res)
