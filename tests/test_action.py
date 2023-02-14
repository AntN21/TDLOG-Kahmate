from game import Game

game=Game()
game.load_json("json_file")

def test():
    width=game.board.width
    height=game.board.height
    for x1 in range(width):
        for y1 in range(height):
            for x2 in range(width):
                for y2 in range(height):
