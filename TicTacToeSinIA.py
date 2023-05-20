import random

#Imprimir el tablero
def draw_board(board):
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[0]} | {board[1]} | {board[2]} ")

# Definir símbolo del jugador
def player_input():
    while True:
        marker = input("Escoge si quieres ser X o O: ").upper()
        if marker in ("X", "O"):
            return marker, "XO".replace(marker, "")

#Poner el símbolo en el tablero
def place_marker(board, marker, position):
    board[position] = marker

# Verificar si alguien ha ganado
def win_check(board, mark):
    return ((board[0] == mark and board[1] == mark and board[2] == mark) or
            (board[3] == mark and board[4] == mark and board[5] == mark) or
            (board[6] == mark and board[7] == mark and board[8] == mark) or
            (board[0] == mark and board[3] == mark and board[6] == mark) or
            (board[1] == mark and board[4] == mark and board[7] == mark) or
            (board[2] == mark and board[5] == mark and board[8] == mark) or
            (board[0] == mark and board[4] == mark and board[8] == mark) or
            (board[2] == mark and board[4] == mark and board[6] == mark))

#Definir quien inicia primero
def choose_first():
    if random.randint(0, 1) == 0:
        return 'Máquina'
    else:
        return 'Jugador'

#Verificar si la posición esta libre
def space_check(board, position):
    return board[position] == ' '

#Verificar tablero
def full_board_check(board):
    for i in range(0, 9):
        if space_check(board, i):
            return False
    return True

def player_choice(board):
    position = 10
    while position not in range(0, 9) or not space_check(board, position):
        try:
            position = int(input('Escoge una posición: (0-8) '))
        except ValueError:
            print("Error, seleccione una entrada válida.")
            continue
        if position not in range(0, 9):
            print("Error, seleccione una entrada en el rango")
            continue
        if not space_check(board, position):
            print("Lo sentimos, esa posición ya está ocupada. Seleccione otra.")
    return position

#Binary search se usa para que el computador escoja la jugada
def binary_search(board, mark):

    for i in range(0, 9, 3):
        if board[i] == mark and board[i+1] == mark and space_check(board, i+2):
            return i+2
        if board[i+1] == mark and board[i+2] == mark and space_check(board, i):
            return i
        if board[i] == mark and board[i+2] == mark and space_check(board, i+1):
            return i+1

    for i in range(0, 3):
        if board[i] == mark and board[i+3] == mark and space_check(board, i+6):
            return i+6
        if board[i+3] == mark and board[i+6] == mark and space_check(board, i):
            return i
        if board[i] == mark and board[i+6] == mark and space_check(board, i+3):
            return i+3

    if board[0] == mark and board[4] == mark and space_check(board, 8):
        return 8
    if board[4] == mark and board[8] == mark and space_check(board, 0):
        return 0
    if board[0] == mark and board[8] == mark and space_check(board, 4):
        return 4

    positions = [4, 0, 2, 6, 8, 1, 3, 5, 7]
    for pos in positions:
        if space_check(board, pos):
            return pos

def tic_tac_toe():
    print('Triqui Juego')
    board = [' '] * 9
    player_marker, computer_marker = player_input()
    turn = choose_first()
    print(turn + ' va a ir primero.')

    while not full_board_check(board):
        if turn == 'Jugador':
            draw_board(board)
            position = player_choice(board)
            place_marker(board, player_marker, position)

            if win_check(board, player_marker):
                draw_board(board)
                print('Felicitaciones ganaste')
                break
            else:
                turn = 'Máquina'
        else:
            draw_board(board)
            print('La máquina va a hacer su jugada...')
            position = binary_search(board, computer_marker)
            place_marker(board, computer_marker, position)

            if win_check(board, computer_marker):
                draw_board(board)
                print('Perdiste. Sigue intentando :D.')
                break
            else:
                turn = 'Jugador'

    if full_board_check(board):
        draw_board(board)
        print('¡Empate!')

tic_tac_toe()