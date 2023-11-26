# OthelloGPT

My reconstruction of [this](https://github.com/likenneth/othello_world)

1. [Generating Data](#generating-data)
2. [Training GPT model](#training-gpt-model)
3. [Training Probes](#training-probes)
4. [Intervention Case Studies](#intervention-case-study)

## Generating Data

Code to simulate games is found within `generate_data.ipynb` and the game logic in `othello.py`. Moves are selected randomly from the set of valid moves (no attempt at learning good moves, only valid moves).

Games are stored as numpy arrays and capped at length $60$.

## Training GPT model

Training loop is in `train.ipynb`. Uses default mingpt training loop edited as in othello_world to train on epochs (sampling without replacement) rather than the default sampling with replacement. Training set used is 1048576 games - took ~ 2 hours to acheive training loss of 2.02 / argmax accuracy of 99.98% training on a 3090 (vast.ai instance). Below is an example of a typical board state with orange squares indicating valid moves that can be taken by black, while on the right is a heatmap of logits output by the model.

![alt text](https://github.com/samm393/OthelloGPT/blob/main/images/img1.png?raw=true)
![alt text](https://github.com/samm393/OthelloGPT/blob/main/images/img2.png?raw=true)

## Training Probes

Probes are trained in `board_probes.ipynb`. They are trained on 100000 games to predict the board state based on activations from each layer. Rather than using the non-linear probes from the original project, linear probes are used using this insight to flip the board state after each turn to reflect 'my piece' vs 'your piece' rather than 'black piece' vs 'white piece'. Below is an example board state on the left and a heatmap showing the most likely category predicted by the probe for each board state (blue = empty, pink = my piece, yellow = opponents piece) with white to play.

![alt text](https://github.com/samm393/OthelloGPT/blob/main/images/img3.png?raw=true)
![alt text](https://github.com/samm393/OthelloGPT/blob/main/images/img4.png?raw=true)

## Intervention Case Study

An example intervention. The white piece in cell (2,1) has its component in the 'opponent (white) direction' removed and a component in the 'black (my) direction' inserted - in this the modification has just been made on the activations coming from the 5th layer, and only only the final token. The original logits output by the model are show on the left, the logits resulting from this intervention on the right. We see that the model has correctly identified that cell (1,0) is no longer a valid move.

![alt text](https://github.com/samm393/OthelloGPT/blob/main/images/img5.png?raw=true)
![alt text](https://github.com/samm393/OthelloGPT/blob/main/images/img6.png?raw=true)
![alt text](https://github.com/samm393/OthelloGPT/blob/main/images/img7.png?raw=true)
