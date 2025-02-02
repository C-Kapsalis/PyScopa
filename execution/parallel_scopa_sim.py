import csv
import subprocess
import threading
from time import sleep
import os
import json  # Added for JSON handling

# Semaphore for thread-safe logging
log_semaphore = threading.Semaphore()

# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate to the simulation folder correctly
scopa_script_path = os.path.join(script_dir, '../simulation/scopa_w_logging.py')
scopa_log_path = os.path.join(script_dir, '../execution/scopa_simulation.log')

def run_game(instance_id):
    """Runs the scopa_w_logging.py script with a unique game instance ID."""
    try:
        subprocess.run(['python', scopa_script_path, f'--instance_id={instance_id}'], check=True)
        with log_semaphore:  # it is != 0, so > 0
            with open(scopa_log_path, 'a') as log_file:
                log_file.write(f'Game {instance_id} completed successfully.\n')
    except subprocess.CalledProcessError as e:
        with log_semaphore:
            with open(scopa_log_path, 'a') as log_file:
                log_file.write(f'Game {instance_id} failed with error: {e}\n')

def parallel_simulate_games(n_games=10000, max_threads=8):
    threads = []

    # Ensure the logs directory exists
    os.makedirs('logs', exist_ok=True)

    for game_num in range(1, n_games + 1):
        thread = threading.Thread(target=run_game, args=(game_num,))
        threads.append(thread)
        thread.start()

        # Limit the number of active threads
        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads = []  # Reset for next batch

    # Wait for any remaining threads to complete
    for t in threads:
        t.join()


if __name__ == "__main__":
    parallel_simulate_games(n_games=10000, max_threads=8)
