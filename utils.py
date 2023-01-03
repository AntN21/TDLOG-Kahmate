def front(team):
    if team=='red':
        return 1
    else:
        return -1

def inbound(board,pos):
    return 0 <= pos[0] and pos[0] < board.length and 0 <= pos[1] and pos[1] <board.width


def neighbours(case):
    res=[]
    for delta0 in [-1,1]:
        for delta1 in [-1,1]:
            res.append([case[0]+delta0,case[1]+delta1])
    return res

def accessibles_cases2(path_length,team,board,position1):
    acc_cases=set(position1)
    new_cases=[]
    for iter in range(path_length):
        for new_case in new_cases:
            acc_cases.add(new_case)
        new_cases = []
        for case in acc_cases:
            for n_case in neighbours(case):
                if inbound(board,n_case):
                    player=board(n_case).player
                    if player is None or player.team == team or player.has_just_lost():
                        new_cases.append(n_case)

def accessibles_cases(path_length, team, board, position1):
    acc_cases = set(tuple(i) for i in [position1])
    new_cases = []
    for iter in range(path_length):
        for new_case in new_cases:
            acc_cases.add(new_case)
        new_cases = []
        for case in acc_cases:
            for n_case in neighbours(case):
                if inbound(board, n_case):
                    player = board(n_case).player
                    if player is None or player.has_just_lost():
                        new_cases.append(tuple(n_case))
    return new_cases
def path_exists(path_length,team,board,position1,position2):
    return position2 in accessibles_cases(path_length,team,board,position1)
