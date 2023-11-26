import numpy as np
import torch as t
import plotly.graph_objects as go
#from show_board import show_board

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
        Othello.show_board(self.board, self.current_player, self.valid_moves())
        
    def display_fig(self):
        return Othello.show_board_fig(self.board, self.current_player, self.valid_moves())
        
    @staticmethod
    def tokens_to_ij(input, padding_val = 0):
        assert input.shape == (61,)
        padded = t.zeros((64,))
        padded[:27] = input[:27]
        padded[27] = padding_val
        padded[28] = padding_val
        padded[29:35] = input[27:33]
        padded[35] = padding_val
        padded[36] = padding_val
        padded[37:] = input[33:-1]
        return padded.reshape(8,8)
    
    @staticmethod
    def token_to_ij(token):
        token_copy = token.copy()
        if token_copy > 26:
            token_copy += 2
        if token_copy > 34:
            token_copy += 2
        return (token_copy // 8, token_copy % 8)
    
    @classmethod
    def flattened_board_states(cls, tokens):
        ctx_len = len(tokens)
        game = cls()
        out = np.zeros((ctx_len,8,8))
        for i in range(ctx_len):
            if tokens[i] == 60:
                game.move_pass()
                continue
            game.move(*cls.token_to_ij(tokens[i].numpy()))
            out[i] = game.board
        return t.tensor(out).view(-1, 64)
    
    @classmethod
    def board_state(cls, tokens, turn):
        game = cls()
        for i in range(turn):
            game.move(*cls.token_to_ij(tokens[i].numpy()))
        game.display()
    
    @staticmethod 
    def pos_to_token(i,j):
        out = 8*i + j
        if out > 36:
            out -= 4
        elif out > 28:
            out -= 2
        return out
    
    @classmethod
    def check_valid_token(cls, input_sequence, next_move):
        game = cls()
        for i in range(input_sequence.shape[0]):
            if input_sequence[i].numpy() == 60:
                game.current_player *= -1
            else:
                game.move(*cls.token_to_ij(input_sequence[i].numpy()))
        return next_move in {cls.pos_to_token(i,j) for i,j in game.valid_moves()}
    
    @staticmethod
    def place_circle(i, j, player, fig):
        if player == 1:
            fig.add_shape(type="circle",
                xref="x", yref="y",
                fillcolor="Black",
                line_color = "Black",
                x0=j+0.15, y0=8-i-1+0.15, x1=j+1-0.15, y1=8-i-0.15,
            )
        elif player == -1:
            fig.add_shape(type="circle",
                xref="x", yref="y",
                fillcolor="White",
                line_color = "White",
                x0=j+0.15, y0=8-i-1+0.15, x1=j+1-0.15, y1=8-i-0.15,
            )
    
    @staticmethod
    def place_rect(i, j, player, fig):
        if player == 1:
            fig.add_shape(type="rect",
                xref="x", yref="y",
                fillcolor="Orange",
                line_color = "Black",
                x0=j, y0=8-i-1, x1=j+1, y1=8-i,
            )
        elif player == -1:
            fig.add_shape(type="rect",
                xref="x", yref="y",
                fillcolor="Orange",
                line_color = "White",
                x0=j, y0=8-i-1, x1=j+1, y1=8-i,
            )
        
    @staticmethod
    def show_board(board, player, valid_moves = None):
        fig = go.Figure()
        fig.update_xaxes(range=[0, 8], showticklabels = False, dtick = 1)
        fig.update_yaxes(range=[0, 8], showticklabels = False, dtick = 1)
        
        for i in range(8):
            for j in range(8):
                if board[i,j] != 0:
                    Othello.place_circle(i, j, board[i,j], fig)
        
        if valid_moves:
            for i, j in valid_moves:
                Othello.place_rect(i, j, player, fig)
                
        
        fig.update_layout(width=400, height=400)

        fig.update_layout(
        margin=dict(l=0,r=0,b=0,t=0),
        paper_bgcolor="Black"
        )
        fig.show()