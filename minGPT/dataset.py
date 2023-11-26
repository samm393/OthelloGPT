from torch.utils.data import Dataset
import torch as t
import numpy as np
from othello import Othello
from tqdm import tqdm

class MyDataset(Dataset):
    def __init__(self, file):
        self.x = t.from_numpy(np.load(file)).long()
    
    def __getitem__(self, index):
        return self.x[index,:-1], self.x[index, 1:]
    
    def __len__(self):
        return self.x.shape[0]
    
class BoardDataset(Dataset):
    def __init__(self, file, flattened_boards_file = None, alternating = False):
        self.x = t.from_numpy(np.load(file)).long()
        
        n_games, n_moves = self.x.shape
        
        self.alternating = alternating
        
        if flattened_boards_file is not None:
            self.flattened_boards = t.from_numpy(np.load(flattened_boards_file))
        
        else:
        
            self.flattened_boards = t.zeros((n_games, n_moves - 1, 64), dtype = t.long)
            for i, tokens in tqdm(enumerate(self.x), total = n_games):
                self.flattened_boards[i] = Othello.flattened_board_states(tokens[:-1]).long()
            self.flattened_boards[self.flattened_boards ==-1] = 2
        
        if alternating:
            #self.flattened_boards[::2][self.flattened_boards[::2] == 1], self.flattened_boards[::2][self.flattened_boards[::2] == 2] = 2, 1
            board_copy = self.flattened_boards.clone().detach()
            self.flattened_boards[:,::2][board_copy[:,::2] == 1], self.flattened_boards[:,::2][board_copy[:,::2] == 2] = 2, 1
            # self.flattened_boards[:,::2] = 0
            # print(self.flattened_boards.shape)
            # print(self.flattened_boards[:,::2].shape)
    
    def __getitem__(self, index):
        
        return self.x[index,:-1], self.x[index, 1:], self.flattened_boards[index]
    
    def __len__(self):
        return self.x.shape[0]
    
    def save_boards(self, file):
        np.save(file, self.flattened_boards)