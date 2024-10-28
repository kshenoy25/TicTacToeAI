import math
import random


class Player():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-9): ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves()) # randomly choose one
        else:
            # get the square based off the minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter # yourself
        other_player = 'O' if player == 'X' else 'X'# other player... so whatever letter is NOT

        # first, check if the previous move is a winner
        # this is the base case
        if state.current_winne == other_player:
            # return position AND score to keep track of the score
            # for minimax to work
            return { 'position': None,
                     'score': 1 * (state.num_empty_square()) if other_player == max_player else -1 * (
                         state.num_empty_square() + 1)
            }
        elif not state.empty_squares(): # no empty squares
            return { 'position': None, 'score': 0}

        # initialize some dictionaries
        if player == max_player:
            best = {'position': None, 'score': -math.inf} # each score should maximize
        else:
            best = {'position': None, 'score': math.inf} # each score should minimize

        for possible_move in state.available_moves():
            # step 1: make a move, try that spot
            state.make_move(possible_move, player)
            # step 2: recurse using minimax to stimulate a game after making that move
            sim_score = self.minimax(state, other_player)
            # step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move # otherwise this will get messed up from the recursion
            # step 4: update the dictionaries if necessary
            if sim_score['score'] > best['score']:
                best =sim_score # replace best
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score # replace best

        return best



