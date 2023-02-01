# Harvest - Optimization Competition
This repository contains the code for the Harvest Optimization Competition. The competition is hosted on [Sharing](https://sharing.cs-campus.fr/compete/62).

## Installation
To use the code, you will need to clone the repository or download the zip file. It is better to clone it as there will be updates during the competition

The code uses only standard Python libraries and pygame. To install pygame, run the following command:
```
pip install pygame
```

## Usage
### For the Reinforcement Learning part
To run the reinforcement learning part, run the following command:
```
python run.py --agent=random
```
You can implement new agents in the `agents` folder. To run your agent, put the name and the import in implemented_agent.py and change the `--agent` argument to the name of your agent.

### For other optimization methods
To see the naive implementation of the optimization problem, run the following command:
```
python naiv_implem.py
```


## Rules

Have Fun !

## The Environment

You control a ship that harvests ressources on its way. The environment is a 10x10 grid that wraps around itself with ressources in each cell. The ship can only move in 2 directions, right or straight ahead. It can only harvest by moving straight. The ressources in each cells are generated with the seed = 42. All ressources are beetwen 0 and 500. The cells containing more than 0 ressources keep their number beetween 10 and 500.
Every turn, the ressource in each cell gains 1.5% and when the ship passes through a cell with ressources, it harvests 40% of the ressources in the cell.

## Contact

If any part of the code is unclear or buggy, please contact me directly on telegram to imrove the code for everyone.