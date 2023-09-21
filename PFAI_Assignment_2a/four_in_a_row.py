'''
Four in a row

Author: Tony Lindgren
'''
from copy import deepcopy

class FourInARow:
    def __init__(self, player, chip):
        new_board = []
        for _ in range(7):
            new_board.append([])
        self.board = new_board
        self.action = list(range(7))
        if chip != 'r' and chip != 'w':
            print('The provided value is not a valid chip (must be, r or w): ', chip)
        if player == 'human' and chip == 'w':
            self.ai_player = 'r'
        else:
            self.ai_player = 'w'
        self.curr_move = chip
    
    def to_move(self):
        return self.curr_move
        
    #actions
    def actions(self):
        return self.action

    def result(self, action):                    
        dc = deepcopy(self)
        dc.action = list(range(7))
        if self.to_move() == 'w':
            dc.curr_move = 'r'
            dc.board[action].append(self.to_move())
            for c in range(0, len(dc.board)):
                if len(dc.board[c]) >=6:
                    if c in dc.action:
                        dc.action.remove(c)
        else:
            dc.curr_move = 'w'
            dc.board[action].append(self.to_move())
            for c in range(0, len(dc.board)):
                if len(dc.board[c]) >=6:
                    if c in dc.action:
                        dc.action.remove(c)
        return dc
        
    #eval
    def eval(self):
        value_matrix = [
            [3, 4, 5, 7, 5, 4, 3],
            [4, 6, 8, 10, 8, 6, 4],
            [5, 8, 11, 13, 11, 8, 5],
            [5, 8, 11, 13, 11, 8, 5],
            [4, 6, 8, 10, 8, 6, 4],
            [3, 4, 5, 7, 5, 4, 3]
        ]

        total_value = 0

        for c in range(7):
            for r in range(len(self.board[c])):
                if self.board[c][r] == self.ai_player:
                    total_value += value_matrix[r][c]

        return total_value
        
    def is_terminal(self):
        #check vertical
        for c in range(0, len(self.board)):
            count = 0
            curr_chip = None
            for r in range(0, len(self.board[c])):
                if curr_chip == self.board[c][r]:
                    count = count + 1
                else:
                    curr_chip = self.board[c][r]     
                    count = 1
                if count == 4:
                    if self.ai_player == curr_chip:        
                        #print('Found vertical win')
                        return True, 100          #MAX ai wins positive utility
                    else:
                        #print('Found vertical loss')
                        return True, -100         #MIN player wins negative utility
                    
        #check horizontal 
        for r in range(0, 6):
            count = 0
            curr_chip = None
            for c in range(0, 7):
                if len(self.board[c]) > r:
                    if curr_chip == self.board[c][r]:
                        count = count + 1
                    else:
                        curr_chip = self.board[c][r]
                        count = 1
                    if count == 4:
                        if self.ai_player == curr_chip:
                            #print('Found horizontal win')
                            return True, 100
                        else:
                            #print('Found horizontal loss')
                            return True, -100
                else:
                    curr_chip = None
                    count = 0

                    
        #check positive diagonal
        for c in range(7-3): 
            for r in range(6-3):    
                if len(self.board[c]) > r and len(self.board[c+1]) > r+1 and len(self.board[c+2]) > r+2 and len(self.board[c+3]) > r+3:
                    if self.ai_player == self.board[c][r] and self.ai_player == self.board[c+1][r+1] and self.ai_player == self.board[c+2][r+2] and self.ai_player == self.board[c+3][r+3]:  
                        #print('Found positive diagonal win')
                        return True, 100
                    elif self.ai_player != self.board[c][r] and self.ai_player != self.board[c+1][r+1] and self.ai_player != self.board[c+2][r+2] and self.ai_player != self.board[c+3][r+3]:  
                        #print('Found positive diagonal loss')
                        return True, -100
        
        #check negative diagonal 
        for c in range(3,7):
            for r in range(6-3):
                if len(self.board[c]) > r and len(self.board[c-1]) > r+1 and len(self.board[c-2]) > r+2 and len(self.board[c-3]) > r+3:
                    if self.ai_player == self.board[c][r] and self.ai_player == self.board[c-1][r+1] and self.ai_player == self.board[c-2][r+2] and self.ai_player == self.board[c-3][r+3]:
                        #print('Found negative diagonal win')
                        return True, 100
                    elif self.ai_player != self.board[c][r] and self.ai_player != self.board[c-1][r+1] and self.ai_player != self.board[c-2][r+2] and self.ai_player != self.board[c-3][r+3]:
                        #print('Found negative diagonal loss')
                        return True, -100


        #check draw
        for c in range(0, len(self.board)):
            if len(self.board[c]) < 6:
                return False, 0
         
        return True, 0
                
    #pretty_print
    def pretty_print(self):
        print('---------------------')
        for r in range(5, -1, -1):
            for c in range(0, 7):
                if len(self.board[c]) > r:
                    print(self.board[c][r], end=' ')
                else:
                    print('_', end=' ')
            print()
        print('---------------------')
