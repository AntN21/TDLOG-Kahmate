"""
Rugby player class file. All players extend this class
"""
from constants import Teams


class RugbyPlayer:
    """
    Contain different properties of a rugby player:1
        - if he is stunt or not (bool stunt);
        - his number of maximum movements (int max_move);
        - his bonuses for attack (int att_bonus) and defence (int def_bonus);
    """

    def __init__(self, player_type, team, max_move, attack_bonus, defense_bonus):
        assert team in (
            Teams.RED,
            Teams.BLUE,
        ), f"{team} is not a correct team color."
        self._type = player_type
        self._team = team
        self._stunned_state = 0
        self._max_move = max_move
        self._attack_bonus = attack_bonus
        self._defense_bonus = defense_bonus
        self._available_moves = self.max_move
        self._just_lost = False

    @property
    def type(self):
        """Returns the source of the player's image"""
        return self._type

    @property
    def team(self):
        """Return the team color of the player"""
        return self._team

    @property
    def stunned(self):
        """Return true if the player is stunned"""
        return self._stunned_state > 0

    @property
    def stunned_state(self):
        """Return the stunned state of a player"""
        return self._stunned_state

    @stunned_state.setter
    def stunned_state(self,s_state):
        """Sets the stunned state of a player."""
        self._stunned_state = s_state

    @property
    def max_move(self):
        """Return the maximum movements the player can do"""
        return self._max_move

    @property
    def attack_bonus(self):
        """Return the attack bonus of the player"""
        return self._attack_bonus

    @property
    def defense_bonus(self):
        """Return the defense bonus of the player"""
        return self._defense_bonus

    @property
    def available_moves(self):
        """Return the number of available moves of the player."""
        return self._available_moves

    @available_moves.setter
    def available_moves(self, avail_moves):
        """Sets the number of available moves of the player."""
        self._available_moves = avail_moves

    def reduce_moves(self, steps):
        """Reduces the moves already made"""
        assert (
            steps <= self.available_moves
        ), "The player has not enough available moves to go that far."
        self.available_moves -= steps

    def set_stunned(self):
        """Turn the player stunning state into 2, ."""
        self._stunned_state = 2

    def recover(self):
        """Decrease the stunned state of the player and removes the "resent lost" state"""
        self.reset_just_lost()
        if self._stunned_state > 0:
            self._stunned_state -= 1

    def reset_moves(self):
        """Reset _available_moves to the maximum number of moves."""
        self._available_moves = self.max_move

    def set_just_lost(self):
        """Set just lost to true"""
        self._just_lost = True

    def reset_just_lost(self):
        """Resets the just lost attribute to false"""
        self._just_lost = False

    def get_just_lost(self):
        """Gets if the player has just lost"""
        return self._just_lost

    def full_reset(self):
        """Reset the state of the player : stunning state and available moves."""
        self.recover()
        self.reset_moves()
        self.reset_just_lost()

    def __str__(self):
        if self.stunned:
            return f"ko_{self.team}"
        return f"{self.type}_{self.team}"
