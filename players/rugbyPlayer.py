from constants import RED_TEAM, BLUE_TEAM

class RugbyPlayer:
    """
    Contain different properties of a rugby player:1
        - if he is stunt or not (bool stunt);
        - his number of maximum movements (int max_move);
        - his bonuses for attack (int att_bonus) and defence (int def_bonus);
    """

    def __init__(self, type, team, max_move, att_bonus, def_bonus):
        assert team == RED_TEAM or team == BLUE_TEAM, f"{team} is not a correct team color."
        self._type = type
        self._team = team
        self._stunned_state = 0
        self._max_move = max_move
        self._att_bonus = att_bonus
        self._def_bonus = def_bonus
        self._available_moves = self.max_move
        self._just_lost = False

    @property
    def type(self):
        """Returns the source of the player's image"""
        return self._type

    @property
    def team(self):
        """Return the team color of the player."""
        return self._team

    @property
    def stunned(self):
        """Return the stunning state of the player."""
        return self._stunned_state > 0

    @property
    def max_move(self):
        """Return the maximum movements the player can do."""
        return self._max_move

    @property
    def att_bonus(self):
        """Return the attack bonus of the player."""
        return self._att_bonus

    @property
    def def_bonus(self):
        """Return the defense bonus of the player."""
        return self._def_bonus

    @property
    def available_moves(self):
        """Return the number of available moves of the player."""
        return self._available_moves

    @available_moves.setter
    def available_moves(self,avail_moves):
        """Return the number of available moves of the player."""
        self._available_moves=avail_moves

    def reduce_moves(self,steps):
        self._available_moves -= steps

    def set_stunned(self):
        """Turn the player stunning state into True."""
        self._stunned_state = 2

    def recover(self):
        """Decrease the stunned state of the player."""
        if self._stunned_state > 0:
            self._stunned_state -= 1

    def move(self, n):
        """Reduce _available_moves of n moves."""
        assert (
            n <= self.available_moves
        ), "The player has not enough available moves to go that far."
        self._available_moves -= n

    def reset_moves(self):
        """Reset _available_moves to the maximum number of moves."""
        self._available_moves = self.max_move

    def lost(self):
        self._just_lost = True

    def reset_lost(self):
        self._just_lost = False

    def has_just_lost(self):
        return self._just_lost

    def full_reset(self):
        """Reset the state of the player : stunning state and available moves."""
        self.recover()
        self.reset_moves()
        self.reset_lost()

    def __str__(self):
        if self.stunned:
            return f"ko_{self.team}"
        return f"{self.type}_{self.team}"
