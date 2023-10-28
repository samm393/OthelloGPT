import numpy as np
from show_board import show_board

class Othello():
    def __init__(self):
        self.board = np.zeros((8,8), dtype=int)
        self.board[3:5,3:5] = np.array([[-1, 1],
                                        [1, -1]])
        self.current_player = 1
        
    def move(self, i, j):
        self.board[i,j] = self.current_player
        
        for a in range(-1,2):
            for b in range(-1,2):
                if a==0 and b==0:
                    continue
                ##looking in direction (a, b)
                k, l = i+a, j+b
                to_be_changed = []
                while 0 <= k and k < 8 and 0 <= l and l < 8 and self.board[k, l] == -1*self.current_player:
                    to_be_changed.append((k, l))
                    k += a
                    l += b
                
                if 0 <= k and k < 8 and 0 <= l and l < 8 and self.board[k, l] == self.current_player:
                    for c, d in to_be_changed:
                        self.board[c, d] = self.current_player
        
        self.current_player *= -1
    
    def move_pass(self):
        self.current_player *= -1
    
    def is_valid_move(self, i, j):
        if self.board[i,j] != 0:
            return False
        
        for a in range(-1,2):
            for b in range(-1,2):
                if a==0 and b==0:
                    continue
                ##looking in direction (a, b)
                k, l = i+a, j+b
                to_be_changed = []
                while 0 <= k and k < 8 and 0 <= l and l < 8 and self.board[k, l] == -1*self.current_player:
                    to_be_changed.append((k, l))
                    k += a
                    l += b
                
                if 0 <= k and k < 8 and 0 <= l and l < 8 and self.board[k, l] == self.current_player:
                    if to_be_changed:
                        return True
        return False
    
    def show_valid_moves(self):
        valid_moves = np.zeros((8,8), dtype=int)
        for i in range(8):
            for j in range(8):
                #print(i,j)
                valid_moves[i,j] = self.is_valid_move(i,j)
        print(valid_moves)
    
    def valid_moves(self):       
        return [(i,j) for i in range(8) for j in range(8) if self.is_valid_move(i,j)]
    
    def display(self):
        show_board(self.board, self.current_player, self.valid_moves())