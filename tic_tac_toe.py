import numpy as np

dictionary = {}
X = 1
O = -1
EMPTY = 0

def check_winner(matrix : np.ndarray[np.float64]):
    diagonal = np.diagonal(matrix)
    anti_diagonal = np.diagonal(np.fliplr(matrix))

    if np.all(diagonal == X) or np.all(anti_diagonal == X):
        return X
    elif np.all(diagonal == O) or np.all(anti_diagonal == O):
        return O
    
    for i in matrix:
        if np.all(i == X):
            return X
        elif np.all(i == O):
            return O
    
    for i in matrix.T:
        if np.all(i == X):
            return X
        elif np.all(i == O):
            return O
        
    return EMPTY

def initialize_ai():
    with open('training_data', 'r') as f:
        for line in f:
            state = line[line.find('['):line.find(']')+1]
            value = line[line.find(']')+5:-1]
            dictionary[state] = value

def i_can_lose(matrix : np.ndarray[np.float64], cpu : int):
    possible_moves = np.where(matrix == EMPTY)
    for i in range(len(possible_moves[0])):
        new_matrix = matrix.copy()
        new_matrix[possible_moves[0][i]][possible_moves[1][i]] = -cpu
        if check_winner(new_matrix) == -cpu:
            return True
    return False

def keyfy(matrix : np.ndarray[np.float64]):
    matrix = [int(item) for sublist in  matrix.tolist() for item in sublist]
    return str(matrix).replace(' ', '')

def get_ai_move(matrix : np.ndarray[np.float64], cpu : int):
    possible_moves = np.where(matrix == EMPTY)
    best_move = None

    if cpu == X:  
        for i in range(len(possible_moves[0])):
            new_matrix = matrix.copy()
            new_matrix[possible_moves[0][i]][possible_moves[1][i]] = cpu
            key = keyfy(new_matrix)
            if best_move is None or dictionary[key] > dictionary[keyfy(best_move)]:
                if not i_can_lose(new_matrix, cpu):
                    best_move = new_matrix
    else:
        for i in range(len(possible_moves[0])):
            new_matrix = matrix.copy()
            new_matrix[possible_moves[0][i]][possible_moves[1][i]] = cpu
            key = keyfy(new_matrix)
            if best_move is None or dictionary[key] < dictionary[keyfy(best_move)]:
                if not i_can_lose(new_matrix, cpu):
                    best_move = new_matrix
    if best_move is None:
        best_move = matrix.copy()
        best_move[possible_moves[0][0]][possible_moves[1][0]] = cpu
    return best_move

def print_field(matrix : np.ndarray[np.float64]):
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == X:
                print('X', end='')
            elif matrix[i][j] == O:
                print('O', end='')
            else:
                print(' ', end='')
            print('|', end='') if j < 2 else print()

def play(player : int):
    field = np.zeros((3,3))
    cpu = -player

    turn = X
    x = None
    y = None

    print("You are playing as", "X" if player == X else "O")
    print("The game starts now!")

    while True:
        if turn == player:
            print_field(field)
            print("Your move: ")
            while True:
                try:
                    x = int(input("x: "))
                    if x < 0 or x > 2:
                        raise ValueError
                    
                    y = int(input("y: "))
                    if y < 0 or y > 2:
                        raise ValueError
                    
                    if field[y][x] == EMPTY:
                        break
                    else:
                        raise PermissionError
                except ValueError:
                    print("Invalid input")
                except PermissionError:
                    print("This field is already taken")
            field[y][x] = player
        else:
            field = get_ai_move(field, cpu)
        if np.all(field != EMPTY):
            print_field(field)
            print("It's a draw!")
            break
        else:
            winner = check_winner(field)
            if winner != EMPTY:
                print_field(field)
                if winner == player:
                    print("You win!")
                else:
                    print("You lose!")
                break
        turn = -turn
        print()






initialize_ai()

while True:
    print("Choose your side: X or O")
    while True:
        side = input()
        if side == 'X' or side == 'O':
            break
    
    side = X if side == 'X' else O
    play(side)
    print("Do you want to play again? (y/n)")
    while True:
        again = input().lower()
        if again == 'y' or again == 'n':
            break
    if again == 'n':
        break