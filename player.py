import math, random

class Player:
    def __init__(self, letter):
        self.letter = letter
        
    def get_move(self, game):
        pass
    
class RandomPlayer(Player):
    def __init__(self, letter):
        super().RandomPlayer.__init__(letter)
        
    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + "'s turn. Input move (0-8): ")
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print("Invalid square.")
        return val

class MiniMaxPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        
    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves()) # randomly select a move if is first player
        else:
            # otherwise pick the best move using MiniMax
            square = self.minimax(game, self.letter)['position']
        return square
    
    # where state is a screenshot of the game at the given arrangement
    def minimax(self, state, player):
        max_player = self.letter # the human player
        min_player = 'O' if player == 'X' else 'X'
        
        if state.current_winner == min_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if min_player == max_player 
                    else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares(): # full board
            return {'position': None, 'score': 0}
        
        if player == max_player:
            best = {'position': None, 'score': -math.inf} # each score should maximise initially
        else:
            best = {'position': None, 'score': math.inf} # each score should minimise initially
        
        for possible_move in state.available_moves():
            # Make a move and try
            state.make_move(possible_move, player)
            
            # Recurse using MiniMax to simulate play from that move
            sim_score = self.minimax(state, min_player)
            
            # Undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move
            
            # Update the dictionaries if applicable
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
                    
        return best