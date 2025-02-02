import os
import subprocess
from time import sleep

# Define script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# File paths
GAME_SCRIPT = os.path.join(script_dir, 'simulation/scopa_w_logging.py')
SIMULATION_LOG = os.path.join(script_dir, 'execution/scopa_simulation.log')
GAME_LOGS_DIR = os.path.join(script_dir, '/logs/')
ANALYSIS_LOG = os.path.join(script_dir, 'scopa_analysis.log')

# # Ensure directories exist
# os.makedirs(os.path.dirname(SIMULATION_LOG), exist_ok=True)
# os.makedirs(os.path.dirname(ANALYSIS_LOG), exist_ok=True)
# os.makedirs(GAME_LOGS_DIR, exist_ok=True)
import os
import json

def save_game_log(instance_id, game_log):
    log_dir = 'logs'
    log_file = f'{log_dir}/game_logs_{instance_id}.json'

    # Ensure the directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Now write the log
    with open(log_file, 'w') as f:
        json.dump(game_log, f, indent=4)


def run_game(instance_id):
    """Runs the scopa_w_logging.py script with a unique game instance ID."""
    save_game_log(instance_id, None)

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
    game_log_path = os.path.join(script_dir, f'logs/game_logs_{instance_id}.json')
    
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
            'board_after': action.get('board_after'),
            'player_1_pile_size': action.get('running_player_1_pile_size'),
            'player_2_pile_size': action.get('running_player_2_pile_size'),
            'player_1_scopas': action.get('running_player_1_scopas'),
            'player_2_scopas': action.get('running_player_2_scopas'),
            'final_player_1_score': int(final_player_1_score),
            'final_player_2_score': int(final_player_2_score)
        }
        actions_analysis.append(analysis)

    analysis_log_file = f'logs/game_{instance_id}_analysis.json'
    with open(analysis_log_file, 'w') as f:
        json.dump(actions_analysis, f, indent=4)


if __name__ == "__main__":
    run_game(1)
    process_game_log(1)