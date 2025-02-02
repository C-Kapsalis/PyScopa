# PyScopa Documentation

## Overview

**PyScopa** is a Python-based simulation and analysis framework designed to model and analyze the Italian card game Scopa. The system simulates multiple games, logs detailed gameplay data, and processes this data to identify winning strategies. The project is structured into distinct modules for simulation, execution, and data analysis.

---

## Project Structure

```
PyScopa/
├── execution/
│   ├── parallel_scopa_proc.py      # Processes game logs concurrently
│   └── parallel_scopa_sim.py       # Simulates multiple games concurrently
├── simulation/
│   ├── scopa_simple.py             # Basic Scopa simulation
│   └── scopa_w_logging.py          # Advanced simulation with detailed logging
├── logs/                           # Stores game logs
├── game_analysis_results.json      # Processed results from simulations
├── scopa_processing.log            # Log file for data processing activities
├── scopa_simulation.log            # Log file for simulation activities
└── README.md                       # Project overview
```

---

## Key Components

### 1. **Simulation Module (`simulation/`)**

- **`scopa_w_logging.py`**: 
  - Simulates a single game of Scopa.
  - Logs each player's actions, board state, captured cards, and pile status.
  - Adds metadata like Scopas scored, Primiera calculations, and final scores.

- **`scopa_simple.py`**:
  - A minimal version for quick simulations without extensive logging.

### 2. **Execution Module (`execution/`)**

- **`parallel_scopa_sim.py`**:
  - Runs multiple simulations in parallel using Python's `threading` module.
  - Manages simulation instances with unique IDs.
  - Dynamically adjusts the file paths to ensure compatibility across environments.

- **`parallel_scopa_proc.py`**:
  - Monitors and processes simulation logs.
  - Uses semaphores for thread-safe logging and queue management.
  - Reads `scopa_simulation.log` to verify completed simulations before processing.

### 3. **Logs and Data**

- **`logs/` Directory**:
  - Contains JSON files generated from each simulation (e.g., `game_logs_1.json`).

- **`scopa_simulation.log`**:
  - Records the success or failure of each simulation.

- **`scopa_processing.log`**:
  - Tracks the status of data processing tasks.

- **`game_analysis_results.json`**:
  - Aggregates insights from processed game logs to identify strategic patterns.

---

## Simulation Details

- **Gameplay Simulation:**
  - Each game logs player actions (e.g., `discard`, `collect_pile`, `capture`).
  - Captures the board state before and after each move.
  - Logs the number of cards with the same `card_value()` in both players' piles.

- **Primiera Calculation:**
  - Follows official Scopa rules.
  - Accounts for suits covered and specific card values.

- **Scopas:**
  - Logged when a player clears the board with a capture.

---

## Processing Workflow

1. **Simulation:**
   - Run `parallel_scopa_sim.py` to start multiple games.
   - Each simulation outputs a JSON log and updates `scopa_simulation.log`.

2. **Processing:**
   - Run `parallel_scopa_proc.py` to process logs.
   - Reads the queue from `processing_queue.log`.
   - Extracts key insights (action efficiency, winning patterns).

3. **Analysis:**
   - Processed data is stored in `game_analysis_results.json`.
   - Used for statistical analysis to derive optimal strategies.

---

## Key Algorithms and Features

- **Concurrency:** Utilizes `threading` for parallel simulations and log processing.
- **Semaphore Synchronization:** Ensures thread-safe operations on log files.
- **Dynamic File Handling:** Automatically adjusts file paths to prevent directory errors.
- **Comprehensive Logging:** Detailed logs for both gameplay and processing steps.

---

## Example Commands

### Run Simulations
```bash
python execution/parallel_scopa_sim.py
```

### Process Game Logs
```bash
python execution/parallel_scopa_proc.py
```

---

## Future Improvements

- **Advanced AI Strategies:** Implement machine learning models to predict optimal moves.
- **Real-time Dashboard:** Visualize simulation results dynamically.
- **Database Integration:** Store logs and results in a scalable database for faster querying.

