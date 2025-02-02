import os
import subprocess
from time import sleep
import json
import threading



# Define script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# File paths
GAME_SCRIPT = os.path.join(script_dir, '../simulation_basis/scopa_w_logging.py')
SIMULATION_LOG = os.path.join(script_dir, '../execution/scopa_simulation.log')
GAME_LOGS_DIR = os.path.join(script_dir, '../logs/')
# ANALYSIS_LOG = os.path.join(script_dir, 'scopa_analysis.log')

# Buffer setup
BUFSIZE = 100
buffer = [-1] * BUFSIZE  # the buffer is a shared resource
nextin = 0  # this is because games have been numbered starting from 1
nextout = 0  # same

# Number of simulation-analysis pairs to run
NITEMS = 100

mutex = threading.Lock()  # lock assuring mutual exclusion - only one thread can modify the buffer at a time
empty = threading.Semaphore(BUFSIZE)  # tracks empty slots in the buffer (aka further game simulations that can take place)
full = threading.Semaphore(0)  # tracks full slots in the buffer (aka further game analyses that can take place)

# Ensure the logs directory exists
os.makedirs('logs', exist_ok=True)

def initialize_game_log(instance_id):
    log_file = f'../logs/game_logs_{instance_id}.json'

    # Now write the log
    with open(log_file, 'w') as f:
        json.dump(None, f, indent=4)


def run_game(instance_id):
    """Runs the scopa_w_logging.py script with a unique game instance ID."""
    initialize_game_log(instance_id)

    try:
        # Run the game script with the provided instance ID
        subprocess.run(['python', GAME_SCRIPT, f'--instance_id={instance_id}'], check=True)
        log_message = f'Game {instance_id} completed successfully.\n'
    except subprocess.CalledProcessError as e:
        log_message = f'Game {instance_id} failed with error: {e}\n'

    # Write the log message to SIMULATION_LOG (creates file if it doesn't exist)
    with open(SIMULATION_LOG, 'a') as log_file:
        log_file.write(log_message)





# Function to process a single game log
def process_game_log(instance_id):
    game_log_path = os.path.join(script_dir, GAME_LOGS_DIR + f'game_logs_{instance_id}.json')
    sleep(0.1)
    with open(game_log_path, 'r') as f:
        game_data = json.load(f)

    actions_analysis = []
    final_input = game_data[-1]
    final_player_1_score = final_input.get('final_player_1_score')
    final_player_2_score = final_input.get('final_player_2_score')
    for action in game_data:
        analysis = {
            'instance_id': int(instance_id),
            'player': action.get('player'),
            'action': action.get('action'),
            'hand': action.get('hand'),
            'board_before': action.get('board_before'),
            'running_card_value_counts': action.get('card_value_counts'),
            'card_played': action.get('card_played'),
            'captured_cards': action.get('captured_cards', None), 
            'cards_collected': action.get('cards_collected', None),
            'board_after': action.get('board_after'),
            'player_1_pile_size': action.get('running_player_1_pile_size'),
            'player_2_pile_size': action.get('running_player_2_pile_size'),
            'player_1_scopas': action.get('running_player_1_scopas'),
            'player_2_scopas': action.get('running_player_2_scopas'),
            'final_player_1_score': int(final_player_1_score),
            'final_player_2_score': int(final_player_2_score)
        }
        actions_analysis.append(analysis)

    analysis_log_file = GAME_LOGS_DIR + f'game_{instance_id}_analysis.json'
    with open(analysis_log_file, 'w') as f:
        json.dump(actions_analysis, f, indent=4)

    


def simulation():
    global nextin
    global buffer
    for instance_id in range(NITEMS):
        empty.acquire()  # decreases the `empty` semaphore - this would make the simulation/`producer` thread to wait in case the buffer is full
        mutex.acquire()  # ensures that only a single simulation/`producer` thread would be able to 
        run_game(instance_id)
        buffer[nextin] = instance_id
        # print(f'Producer: produced {instance_id} in slot {nextin}')
        nextin = (nextin + 1) % BUFSIZE
        mutex.release()
        full.release()


def analysis():
    global nextout
    global buffer
    for i in range(NITEMS):
        full.acquire()
        mutex.acquire()
        instance_id = buffer[nextout]
        process_game_log(instance_id)
        # print(f'Consumer: consumed {instance_id} from slot {nextout}')
        nextout = (nextout + 1) % BUFSIZE
        mutex.release()
        empty.release()




if __name__ == "__main__":
    t1 = threading.Thread(target=simulation)
    t2 = threading.Thread(target=analysis)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
