import math, random

"""
The class Player. This is the template for all the types of players. Contains a 
constructor and the means to get the move to play.
"""
class Player:
    def __init__(self, letter):
        self.letter = letter
        
    def get_move(self, game):
        pass
    
"""
The class RandomPlayer. This is for when a computer controlled player should randomly
select the available move to play.
"""
class RandomPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        
    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square

"""
The class HumanPlayer. This is for when a user controlled player is desired and the
user will enter an integer between 0-8 to represent the tile to place their respective
naught or cross.
"""
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

"""
The class MiniMaxPlayer. This is for when the computer controlled player selects the best 
possible move using the MiniMax algorithm. This ensures that the player will maximise their 
move while minimizing the opponents move. From this it makes it impossible to beat a player 
with the best outcome being a tie from perfect play.
"""
class MiniMaxPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        
    def get_move(self, game):
        if len(game.available_moves()) == 9:
            # If the player is first to move, all square haves the same score so no need to compute.
            square = random.choice(game.available_moves())
        else:
            # Otherwise pick the best move using MiniMax.
            square = self.minimax(game, self.letter)['position']
        return square
    
    def minimax(self, state, player):
        max_player = self.letter 
        min_player = 'O' if player == 'X' else 'X'
        
        if state.current_winner == min_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if min_player == max_player 
                    else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}
        
        if player == max_player:
            # Each score should maximise initially.
            best = {'position': None, 'score': -math.inf} 
        else:
            # Each score should minimise initially.
            best = {'position': None, 'score': math.inf} 
        
        for possible_move in state.available_moves():
            # Make a move and try.
            state.make_move(possible_move, player)
            
            # Recurse using MiniMax to simulate play from that move.
            sim_score = self.minimax(state, min_player)
            
            # Undo the move.
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move
            
            # Update the dictionaries if applicable.
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
                    
        return best
    