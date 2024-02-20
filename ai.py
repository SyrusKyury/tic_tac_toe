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


def save_state(matrix : np.ndarray[np.float64], winner : int):
    for i in range(4):
            matrix = np.rot90(matrix)
            dictionary[str(matrix)] = winner
            dictionary[str(np.fliplr(matrix))] = winner
            dictionary[str(np.flipud(matrix))] = winner
            dictionary[str(np.fliplr(np.flipud(matrix)))] = winner

def train(matrix = np.zeros((3,3)), player = X):

    winner = check_winner(matrix)
    if winner != EMPTY:
        save_state(matrix, winner)
        return winner
    
    possible_moves = np.where(matrix == 0)
    if len(possible_moves[0]) == 0:
        save_state(matrix, EMPTY)
        return EMPTY
    
    state = 0
    for i in range(len(possible_moves[0])):
        new_matrix = matrix.copy()
        new_matrix[possible_moves[0][i]][possible_moves[1][i]] = player
        if not (str(new_matrix) in dictionary):
            winner = train(new_matrix, -player)
            save_state(matrix, winner)
        else:
            winner = dictionary[str(new_matrix)]
        
        
        state += winner

    save_state(matrix, state/len(possible_moves[0]))
    return state/len(possible_moves[0])

    

train()

with open('training_data', 'w') as file:
    for key, value in dictionary.items():
        key = key.replace('[', '')
        key = key.replace(']', '')
        key = key.replace('\n', '')
        key = key.replace('.', '')
        key = key.replace('  ', ' ')
        key = key.replace(' ', ',')
        key = key[1:] if key[0] == ',' else key
        file.write("[" + key + ']' + " => " + str(float(value)) + '\n')