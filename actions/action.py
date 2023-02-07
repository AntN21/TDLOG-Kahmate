"""
Action file
"""


class Action:
    """
    Represent th differents actions.
    It has two parameters which are lists of 2 ints representing squares:
        -position1 represents the square from which the action is done
        -position2 represents the square targeted by the action
    """

    def __init__(self, position1, position2):
        self._position1 = position1
        self._position2 = position2

    @property
    def position1(self):
        """Return the position of origin"""
        return self._position1

    @property
    def position2(self):
        """Return the targeted position"""
        return self._position2

    def to_dict(self):
        """Serializes the class as a dictionary"""
        res = {}
        res["position_1"] = self.position1
        res["position_2"] = self.position2
        return res
