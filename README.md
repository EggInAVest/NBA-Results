# NBA Stats Terminal App

A Python command-line application for viewing NBA game results, standings, league leaders, and tracking a custom betting leaderboard.

## Features

- **Last Night's Results (Overview)**: Quick view of game scores with color-coded winners
- **Last Night's Results (Detailed)**: Complete box scores with player statistics
- **Season Standings**: Current standings for both Eastern and Western conferences
- **League Leaders**: Top 5 players in points, rebounds, assists, blocks, and steals
- **Bet Leaderboard**: Custom scoring system tracking multiple players' team predictions

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation & Setup

### 1. Clone or Download the Project

Download the project files to your local machine and navigate to the project directory.

### 2. Create a Virtual Environment

A virtual environment isolates your project dependencies from other Python projects on your system.

**On Windows:**
```bash
python -m venv venv
```

**On macOS/Linux:**
```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt, indicating the virtual environment is active.

### 4. Install Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

With the virtual environment activated, run:

```bash
python main.py
```

You'll see a menu with 6 options. Enter the number corresponding to your choice and press Enter.

## Deactivating the Virtual Environment

When you're done using the app, deactivate the virtual environment:

```bash
deactivate
```

## Dependencies Explained

Here's what each package in `requirements.txt` does:

- **certifi** (2025.11.12): Provides SSL certificates for secure HTTPS connections
- **charset-normalizer** (3.4.4): Detects and normalizes character encodings when reading web data
- **idna** (3.11): Handles internationalized domain names (non-ASCII URLs)
- **nba_api** (1.11.3): The core library that provides access to NBA statistics and data
- **numpy** (2.3.5): Numerical computing library used by pandas for data manipulation
- **pandas** (2.3.3): Data analysis library used to handle NBA statistics in table format
- **python-dateutil** (2.9.0.post0): Provides powerful extensions for working with dates and times
- **pytz** (2025.2): World timezone definitions for Python
- **requests** (2.32.5): Makes HTTP requests to fetch NBA data from web APIs
- **six** (1.17.0): Python 2 and 3 compatibility library (dependency of other packages)
- **tzdata** (2025.2): Timezone database for accurate time handling
- **urllib3** (2.5.0): HTTP library that powers the requests package

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'nba_api'`  
**Solution**: Make sure your virtual environment is activated and you've run `pip install -r requirements.txt`

**Issue**: No games showing in "Last night's results"  
**Solution**: The app fetches games from "today's scoreboard". If no games have been played yet today, try running it after games have started or finished.

**Issue**: API errors or timeouts  
**Solution**: The app relies on external NBA APIs. Check your internet connection and try again in a few moments.

## Notes

- The betting leaderboard feature tracks specific teams for specific players (Roni, Rasmus, Tony, Sakari, and Tomi). You can modify these in the `getBetLeaderboard()` function to track your own teams.
- Color coding in the terminal uses ANSI escape codes and works best on modern terminal emulators.
- Data is fetched in real-time from NBA's official APIs, so an internet connection is required.

## License

This is a personal project. Feel free to modify and use it for your own purposes.
