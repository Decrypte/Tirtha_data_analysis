import json

def save_checkpoint(state, filename="checkpoint.json"):
    with open(filename, 'w') as f:
        json.dump(state, f)

def load_checkpoint(filename="checkpoint.json"):
    try:
        with open(filename, 'r') as f:
            state = json.load(f)
    except FileNotFoundError:
        state = {'i': 1, 'j': 1, 'k': 1}  # default starting point
    return state


