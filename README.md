# PyScopa Documentation

## Overview

**PyScopa** is a Python-based simulation and analysis framework designed to model and analyze the Italian card game Scopa. The system simulates multiple games, logs detailed gameplay data, and processes this data to identify winning strategies. The project is structured into distinct modules for simulation, execution, and data analysis.

---

## Project Structure

```
PyScopa/
├── execution/
│   ├── simple_parallelization.py   # Processes and analyzes game logs concurrently
│   └── scopa_simulation.log            # Log file for simulation activities
├── simulation/
│   ├── scopa_simple.py             # Basic Scopa simulation
│   └── scopa_w_logging.py          # Advanced simulation with detailed logging
├── logs/                           # Stores game logs (logs of simulations / logs of analyses)
├── analysis/                       # Stores algos used to aggregate insights from processed game logs to identify strategic patterns.
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

- **`simple_parallelization.py`**:
  - Runs multiple simulations and game analyses in parallel using Python's `threading` module.
  - Manages simulation/analysis instances with unique IDs.
  - Dynamically adjusts the file paths to ensure compatibility across environments.


### 3. **Logs and Data**

- **`logs/` Directory**:
  - Contains JSON files generated from each simulation and game analysis (e.g., `game_logs_1.json`, `game_logs_1_analysis.json`).

- **`scopa_simulation.log`**:
  - Records the success or failure of each simulation.

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
   - Run `parallel_scopa_sim.py` to start and analyze multiple games.
   - Each simulation outputs a JSON log and updates `scopa_simulation.log` and the `logs` folder.

2. **Analysis:**
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
python execution/simple_parallelization.py
```

### Analyze results
```bash
python analysis/???
```

---

## Future Improvements

- **Advanced AI Strategies:** Implement machine learning models to predict optimal moves.
- **Real-time Dashboard:** Visualize simulation results dynamically.
- **Database Integration:** Store logs and results in a scalable database for faster querying.

