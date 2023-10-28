import plotly.graph_objects as go
import numpy as np

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
    

def show_board(board, player, valid_moves = None):
    fig = go.Figure()
    fig.update_xaxes(range=[0, 8], showticklabels = False, dtick = 1)
    fig.update_yaxes(range=[0, 8], showticklabels = False, dtick = 1)
    
    for i in range(8):
        for j in range(8):
            if board[i,j] != 0:
                place_circle(i, j, board[i,j], fig)
    
    if valid_moves:
        for i, j in valid_moves:
            place_rect(i, j, player, fig)
            
    
    fig.update_layout(width=400, height=400)

    fig.update_layout(
    margin=dict(l=0,r=0,b=0,t=0),
    paper_bgcolor="Black"
    )
    fig.show()
    
# board = np.zeros((8,8), dtype=int)
# board[3:5,3:5] = np.array([[-1, 1],
#                             [1, -1]])

# valid_moves = [(1,1),(2,2)]

# show_board(board, valid_moves)