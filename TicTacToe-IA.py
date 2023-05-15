import tkinter as tk
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.tree import _tree
from sklearn.model_selection import GridSearchCV

board = [" "] * 9 # create an empty board
symbols = ["X", "O"] # symbols for players
turn = 0 # keep track of whose turn it is

# check if the board is full
def is_full():
    return " " not in board

# check if a player has won
def has_won(symbol):
    # check rows, columns and diagonals
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # columns
        [0, 4, 8], [2, 4, 6] # diagonals
    ]
    for pattern in win_patterns:
        if all(board[i] == symbol for i in pattern):
            return True
    return False




# get the best move for the AI using decision tree
def get_ai_move(symbol):
    # get the opposite symbol of the AI
    opponent = symbols[(symbols.index(symbol) + 1) % 2]
    # get the list of empty positions on the board
    empty_positions = [i for i in range(9) if board[i] == " "]
    
    # import the dataset from the csv file
    dataset = pd.read_csv('tic-tac-toe-endgame.csv')
    
    # encode the categorical variables using LabelEncoder
    X = dataset.iloc[:, :-1].values # features (board state)
    y = dataset.iloc[:, -1].values # labels (win/loss/tie)
    
    labelencoders_X = []
    for i in range(X.shape[1]):
        labelencoder_X = LabelEncoder()
        labelencoder_X.fit(np.append(X[:, i], np.append(symbols, " ")))
        X[:, i] = labelencoder_X.transform(X[:, i])
        labelencoders_X.append(labelencoder_X)
    
    labelencoder_y = LabelEncoder()
    y = labelencoder_y.fit_transform(y)
    
    # scale X using StandardScaler
    sc = StandardScaler()
    X = sc.fit_transform(X)
    
    # create a decision tree classifier for the AI
    classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
    
    # fit the classifier to the entire dataset
    classifier.fit(X, y)
    
     # find rows in dataset that are most similar to current board state
    current_board_encoded = []
    for i in range(len(board)):
         current_board_encoded.append(labelencoders_X[i].transform([board[i]])[0])
    current_board_scaled = sc.transform([current_board_encoded])[0]
     
    distances = []
    for i in range(X.shape[0]):
         distance = np.linalg.norm(current_board_scaled - X[i])
         distances.append((i, distance))
     
    distances.sort(key=lambda x: x[1])
     
    num_rows_to_print = 5
    print(f"{num_rows_to_print} rows in dataset that are most similar to current board state:")
    for i in range(num_rows_to_print):
         row_index, distance = distances[i]
         row_data = dataset.iloc[row_index]
         print(f"Row {row_index} (distance = {distance}): {row_data}")
     
     # generate all possible next board states for the AI
    next_states = []
    for pos in empty_positions:
         next_board = board.copy()
         next_board[pos] = symbol
         next_states.append(next_board)

     # encode next_states using labelencoders_X
    next_states_encoded = []
    for state in next_states:
         state_encoded = []
         for i in range(len(state)):
             state_encoded.append(labelencoders_X[i].transform([state[i]])[0])
         next_states_encoded.append(state_encoded)

     # scale next_states_encoded using sc
    next_states_scaled = sc.transform(next_states_encoded)

     # predict outcomes and probabilities for all possible next states using classifier
    outcomes = classifier.predict(next_states_scaled)
    probabilities = classifier.predict_proba(next_states_scaled)

     # print outcomes and probabilities for all possible next states
    print("Outcomes and probabilities for all possible next states:")
    for state, outcome, probability in zip(next_states, outcomes, probabilities):
         outcome_str = 'loss' if outcome == 0 else 'win'
         probability_str = f"{probability[outcome]*100:.1f}%"
         print(f"{state}: {outcome_str} ({probability_str})")

     # get index of best outcome for AI
    best_outcome_index = outcomes.argmax()

     # get best move for AI
    best_move = empty_positions[best_outcome_index]

     
     # print best move and probability
    best_outcome_str = 'loss' if outcomes[best_outcome_index] == 0 else 'win'
    best_probability_str = f"{probabilities[best_outcome_index][outcomes[best_outcome_index]]*100:.1f}%"
    print(f"Best move: {best_move} ({best_outcome_str}, {best_probability_str})")
     
    return best_move




# create the main window
window = tk.Tk()
window.title("TicTacToe")

# create a label to display the current player's turn
turn_label = tk.Label(window, text="Player X's turn")
turn_label.pack()

# create a frame to hold the buttons
board_frame = tk.Frame(window)
board_frame.pack()

# create a function to handle button clicks
def handle_click(i):
    global turn
    symbol = symbols[turn % 2]
    if board[i] == " ":
        board[i] = symbol
        buttons[i].config(text=symbol)
        if has_won(symbol):
            turn_label.config(text=f"Player {symbol} has won!")
            for button in buttons:
                button.config(state=tk.DISABLED)
        elif is_full():
            turn_label.config(text="It's a tie!")
        else:
            turn += 1
            symbol = symbols[turn % 2]
            if symbol == "O":
                ai_move = get_ai_move(symbol)
                board[ai_move] = symbol
                buttons[ai_move].config(text=symbol)
                if has_won(symbol):
                    turn_label.config(text=f"Player {symbol} has won!")
                    for button in buttons:
                        button.config(state=tk.DISABLED)
                elif is_full():
                    turn_label.config(text="It's a tie!")
                else:
                    turn += 1
                    symbol = symbols[turn % 2]
            turn_label.config(text=f"Player {symbol}'s turn")

# create a list of buttons for the board
buttons = []
for i in range(9):
    button = tk.Button(board_frame, text=" ", width=3, height=1, font=("Helvetica", 24), command=lambda i=i: handle_click(i))
    row, col = divmod(i, 3)
    button.grid(row=row, column=col)
    buttons.append(button)

# run the main loop
window.mainloop()


