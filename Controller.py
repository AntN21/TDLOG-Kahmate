import constants
class Controller:
    def __init__(self):
        pass
    def get_square(self):
        pass
    def get_card(self):
        pass

    def get_action(self):
        pass

    def get_any(self):
        pass

class Console(Controller):

    def get_square(self):
        print(f'Choose a square')
        x_input=int(input(f'Put the abciss first'))
        y_input=int(input(f'Put the ordinate now'))
        return (x_input,y_input)

    def get_card(self):
        return int(input("Choose a card."))

    def get_action(self):
        print(f'{constants.ACTION_ORDER_LIST}')
        return int(input(f'Choose a number corresponding to your action (starting from 0).\n'))


