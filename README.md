# Dark Ages Syraxius Bot

## Disclaimer and notes:
- This hunting bot is for educational purposes only.
- This is a beta software, and may stay beta forever.
- This requires some slight knowledge in cmd and Python to install, configure and run (learn Python :D).
- I am not responsible for any consequences resulting from the usage of this bot.

## Features:
- Automatic hunting for assail-based classes (Warrior, Monk) and spell-based classes (Wizard).
- Extremely stable. Got my Warrior and Wizard from level 1 to 65 within 5 days in Crypt 1-1 to Crypt 3-1.
- Accurate spell-casting even on enemies behind walls.
- Rest when HP or MP is below threshold (set `mp_low`, `hp_low`, `mp_high`, `hp_high`).
- Maintain minimum distance from nearest enemy (set `run_start_dist`, `run_stop_dist`).
- Intelligent Pathfinding to choose the safest possible route when enemies are near.
- Patrol maps to search for monsters when hunting.
- Travel between maps when resting and hunting.

## Installation (for Windows):
- Clone this repository (or download this repository and extract it somewhere)
- Install Python 3.9 from https://www.python.org/
- Create a Python 3.9 virtual environment in this folder using `python3 -m venv venv`
- Activate your virtual environment using `cd venv/Scripts && activate`
- Install requirements listed in requirements.txt using `pip install -r requirements.txt`
- (Personally, I just use PyCharm IDE for all these)

## Configuration:
- Configure parameters in configs folders (mainly `configs/user.py`, but you may also tweak `configs/map.py`)

## Running:
- Ensure that your cilent resolution is at the default 1280x960
- Ensure that your map is open, and is at default zoom levels
- Ensure that your play area is enlarged (press `/` or click on the green button on the lower right)
- Activate your virtual environment and run `main.py`
