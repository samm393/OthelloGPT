"""
Simple training loop; Boilerplate that could apply to any arbitrary neural network,
so nothing in this file really has anything to do with GPT specifically.
"""

import time
from collections import defaultdict

import torch
from torch.utils.data.dataloader import DataLoader
from mingpt.utils import CfgNode as CN

from tqdm import tqdm

class Trainer:

    @staticmethod
    def get_default_config():
        C = CN()
        # device to train on
        C.device = 'auto'
        # dataloder parameters
        C.num_workers = 4
        # optimizer parameters
        C.max_iters = None
        C.batch_size = 64
        C.learning_rate = 3e-4
        C.betas = (0.9, 0.95)
        C.weight_decay = 0.1 # only applied on matmul weights
        C.grad_norm_clip = 1.0
        C.max_epochs = 250
        C.sub_epoch = False
        return C

    def __init__(self, config, model, train_dataset, val_dataset):
        self.config = config
        self.model = model
        self.optimizer = None
        self.train_dataset = train_dataset
        self.val_dataset = val_dataset
        self.callbacks = defaultdict(list)

        # determine the device we'll train on
        if config.device == 'auto':
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = config.device
        self.model = self.model.to(self.device)
        print("running on device", self.device)

        
    def run_epoch(self, model, config):
        train_loader = DataLoader(
            self.train_dataset,
            shuffle=True,
            pin_memory=True,
            batch_size=config.batch_size,
            num_workers=config.num_workers,
        )

        model.train()
        pbar = tqdm(enumerate(train_loader), total = len(train_loader))
        
        for it, (x, y) in pbar:

            # fetch the next batch (x, y) and re-init iterator if needed

            # forward the model
            logits, self.loss = model(x.to(self.device), y.to(self.device))

            # backprop and update the parameters
            model.zero_grad(set_to_none=True)
            self.loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), config.grad_norm_clip)
            self.optimizer.step()
            pbar.set_description(f"iter {it}, training_loss = {self.loss}")
            
        val_loader = DataLoader(
            self.val_dataset,
            shuffle=True,
            pin_memory=True,
            batch_size=config.batch_size,
            num_workers=config.num_workers,
        )
        
        pbar = tqdm(enumerate(val_loader), total = len(val_loader))
        
        for it, (x, y) in pbar:

            # fetch the next batch (x, y) and re-init iterator if needed

            # forward the model
            logits, val_loss = model(x.to(self.device), y.to(self.device))

            # backprop and update the parameters
            pbar.set_description(f"iter {it}, val_loss = {val_loss}")

    
    def run(self):
        model, config = self.model, self.config

        # setup the optimizer
        self.optimizer = model.configure_optimizers(config)


        for epoch in range(config.max_epochs):
                print(f'Epoch {epoch}')
                self.run_epoch(model, config)

        # if config.sub_epoch:
        #     for sub_epoch in range(10):
        #         self.train_dataset
        #     for epoch in range(config.max_epochs):
        #         print(f'Epoch {epoch}')
        #         self.run_epoch(model, config)
        # else:
        #     for epoch in range(config.max_epochs):
        #         print(f'Epoch {epoch}')
        #         self.run_epoch(model, config)