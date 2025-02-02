import json
import os


# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate to the simulation folder correctly
SIMULATION_LOG = os.path.join(script_dir, '../execution/scopa_simulation.log')
# Path to the simulation log and the directory with game logs
GAME_LOGS_DIR = os.path.join(script_dir, '../logs/')
ANALYSIS_LOG = os.path.join(script_dir, '../execution/scopa_analysis.log')

# Function to read successfully completed game IDs
def get_successful_game_ids():
    successful_ids = set()
    with open(SIMULATION_LOG, 'r') as log_file:
        for line in log_file:
            if 'completed successfully' in line:
                game_id = line.strip().split()[1]
                successful_ids.add(game_id)
    return successful_ids

# Function to process a single game log
def process_game_log(file_path, instance_id):
    with open(file_path, 'r') as f:
        game_data = json.load(f)

    actions_analysis = []
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
        }
        actions_analysis.append(analysis)

    return actions_analysis

# Function to analyze all successful game logs
def analyze_successful_games():
    successful_ids = get_successful_game_ids()
    all_analyses = []

    for instance_id in successful_ids:
        file_path = os.path.join(GAME_LOGS_DIR, f'game_logs_{instance_id}.json')
        if os.path.exists(file_path):
            analysis = process_game_log(file_path, instance_id)
            all_analyses.extend(analysis)

    return all_analyses

if __name__ == "__main__":
    analyses = analyze_successful_games()

    # Example: save the analysis to a JSON file
    with open(ANALYSIS_LOG, 'w') as outfile:
        json.dump(analyses, outfile, indent=4)

    print(f"Processed {len(analyses)} actions from successful games.")
