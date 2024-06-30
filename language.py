import os
import pickle

STATE_FILE = os.getenv("STATE_FILE")


def load_state():
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'rb') as f:
                return pickle.load(f)
        else:
            return {}
    except:
        return {}


def save_state(state):
    with open(STATE_FILE, 'wb') as f:
        pickle.dump(state, f)


def get_selected_language(user_id):
    state = load_state()
    lang = state.get(user_id)
    return lang
