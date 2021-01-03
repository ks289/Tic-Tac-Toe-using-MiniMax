import time
from player import HumanPlayer, MiniMaxPlayer, RandomPlayer

"""
The class TicTacToe. This handles the playing of the game, including the displaying
of the game and gathering information on the current state of the game.
"""
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        
    """
    This will print the board in a human readable format.
    """
    def print_board(self):
        for row in [self.board[i * 3: (i + 1) * 3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")
            
    """
    This prints the initial board arrangement so the user can understand the 
    numbering for each tile. 
    """
    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print("| " + " | ".join(row) + " |")
            
    """
    This finds all the available in the current state of the board.
    Returns:
        This will return a list of all the available moves.
    """
    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']
        
    """
    This finds all the empty tiles (squares) in the current state of the board.
    Returns:
        This will return a list of all the empty squares on the board.
    """
    def empty_squares(self):
        return " " in self.board
    
    """
    This gives a number of these empty squares.
    Returns:
        This will return the number of empty squares on the board.
    """
    def num_empty_squares(self):
        return len(self.available_moves())
    
    """
    This will make the move given that it is valid and detect if the move resulted in the 
    current player winning the game.
    Returns:
        This will return True if the move was made and False otherwise.
    """
    def make_move(self, square, letter):
        if self.board[square] == " ":
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    """
    This will check if the current player is a winner by checking if there is a chain of 3 letters in
    either a row, column or one of the two diagonals.
    Returns:
        This will return True if the current player won the game or False otherwise.
    """
    def winner(self, square, letter):
        # Checking for row.
        row_ind = square // 3
        row = self.board[row_ind * 3 : (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True
        
        # Checking for column.
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all ([spot == letter for spot in column]):
            return True
        
        # Checking for diagonal
        if square % 2 == 0:
            # Left to right diagonal.
            diagonal1 = [self.board[i] for i in [0, 4, 8]] 
            if all ([spot == letter for spot in diagonal1]):
                return True
             # Right to left diagonal.
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all ([spot == letter for spot in diagonal2]):
                return True
        
        return False

"""
This is the main game loop which will prompt the player to enter a move while 
the game isn't over.
"""
def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()
        
    letter = 'X'
    # Iterate while game is incomplete.
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(letter + f" makes a move to square {square}")
                game.print_board()
                print("")
            
            if game.current_winner:
                if print_game:
                    print(letter + " wins!")
                return letter
                
            letter = "O" if letter == "X" else "X"
            
        # Tiny break to make more human readable.
        time.sleep(1)
    
    if print_game:
        print("It's a tie.")

if __name__ == '__main__':
    x_player = HumanPlayer('X')
    o_player = MiniMaxPlayer('O')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)