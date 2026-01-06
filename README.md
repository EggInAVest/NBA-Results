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

## License

This is a personal project. Feel free to modify and use it for your own purposes.
