import json
import os

# Path to the simulation log and the directory with game logs
SIMULATION_LOG = 'scopa_simulation.log'
GAME_LOGS_DIR = 'logs'

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
def process_game_log(file_path):
    with open(file_path, 'r') as f:
        game_data = json.load(f)

    actions_analysis = []
    for action in game_data:
        analysis = {
            'player': action.get('player'),
            'action': action.get('action'),
            'hand': action.get('hand'),
            'board_before': action.get('board_before'),
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

    for game_id in successful_ids:
        file_path = os.path.join(GAME_LOGS_DIR, f'game_logs_{game_id}.json')
        if os.path.exists(file_path):
            analysis = process_game_log(file_path)
            all_analyses.extend(analysis)

    return all_analyses

if __name__ == "__main__":
    analyses = analyze_successful_games()

    # Example: save the analysis to a JSON file
    with open('game_analysis_results.json', 'w') as outfile:
        json.dump(analyses, outfile, indent=4)

    print(f"Processed {len(analyses)} actions from successful games.")
