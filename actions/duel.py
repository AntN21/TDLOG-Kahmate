"""
File containing the duel class
"""
from constants import Teams
from actions.action import Action


class Duel(Action):
    """
    Contains the duel information (both players chosen cards and the continuous duel
    number (one can tie a first duel, but the second tie will result in the defending
    team as a winner)
    """

    def __init__(self, position1, position2, duel_number=0):
        super().__init__(position1, position2)
        self._attacker_choice = None
        self._defender_choice = None
        self._duel_number = duel_number

    def choose_card(self, game, card, team):
        """
        Sets the chosen card of one of the teams
        """
        if team == game.board(self.position1).player.team:
            self._attacker_choice = card
        else:
            self._defender_choice = card

    def is_ready(self):
        """
        Returns true if both players have chosen their cards
        """
        return self._attacker_choice is not None and self._defender_choice is not None

    def play(self, game):
        """
        Executes the duel, returning the duel data as a tuple of the winner,
        the defensor's score and the attacker's score
        """
        attacker = game.board(self.position1).player.team
        assert attacker == game.team_playing
        card1, card2 = self._attacker_choice, self._defender_choice
        game.teams[attacker].cards.remove(self._attacker_choice)
        game.teams[Teams.RED.other(attacker)].cards.remove(self._defender_choice)
        if len(game.teams[attacker].cards) == 0:
            game.teams[attacker].cards = list(range(1, 6 + 1))
            game.teams[Teams.RED.other(attacker)].cards = list(range(1, 6 + 1))
        player1 = game.board(self.position1).player
        player2 = game.board(self.position2).player
        score_attack = card1 + player1.attack_bonus
        score_defense = card2 + player2.defense_bonus
        if score_attack > score_defense:
            return (attacker, score_attack, score_defense)
        if score_defense > score_attack:
            return (Teams.RED.other(attacker), score_defense, score_attack)
        if self._duel_number >= 0:
            return None
        return (Teams.RED.other(attacker), score_defense, score_attack)
