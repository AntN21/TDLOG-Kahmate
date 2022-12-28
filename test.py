import game


def test_move_player():
    player = game.Clever("red")
    board = game.Board()
    x = 6
    y = 2
    x2 = 9
    y2 = 4

    board.put_player(player, x, y)
    board.move_player(x, y, x2, y2)

    assert board.square(x, y).player is None
    assert isinstance(board.square(x2, y2).player, game.Clever)


# Not a good test
def test_board_str():
    game_test = game.Game(random=True)

    x_ball, y_ball = (game_test.board.width // 2, 0)
    x_player, y_player = (0, 0)
    for y in range(game_test.board.height):
        if game_test.board([x_ball, y]).ball:
            y_ball = y
        if game_test.board([1, y]).player is not None:
            x_player = 1
            y_player = y
        if game_test.board([2, y]).player is not None:
            x_player = 2
            y_player = y

    game_test.board.move_ball(x_ball, y_ball, x_player, y_player)

    print(game_test.board)
