# OthelloGPT

My reconstruction of [this](https://github.com/likenneth/othello_world)

1. [Generating Data](#generating-data)
2. [Training GPT model](#training-gpt-model)
3. [Training Probes](#training-probes)
4. [Intervention Case Studies](#intervention-case-studies)

## Generating Data

Code to simulate games is found within `generate_data.ipynb` and the game logic in `othello.py`. Moves are selected randomly from the set of valid moves (no attempt at learning good moves, only valid moves).

Games are stored as numpy arrays and capped at length $60$.

## Training GPT model

Training loop is in `train.ipynb`. Uses default mingpt training loop edited as in othello_world to train on epochs (sampling without replacement) rather than the default sampling with replacement. Training set used is 1048576 games - took ~ 2 hours to acheive training loss of 2.02 / argmax accuracy of 99.98% training on a 3090 (vast.ai instance)

## Training Probes

Probes are trained in `board_probes.ipynb`. They are trained on 100000 games to predict the board state based on activations from each layer. Rather than using the non-linear probes from the original project, linear probes are used using this insight to flip the board state after each turn to reflect 'my piece' vs 'your piece' rather than 'black piece' vs 'white piece'

## Intervention Case Studies
