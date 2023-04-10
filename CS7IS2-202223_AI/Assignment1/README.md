## Note
The entry to the program is in main.py, which supports 4 parameters:
```sh
`--rows`: The rows (row number) of maze.

`--cols`: The cols (column number) of maze.

`--solver`: The algorithm of solver, you can choose `['bfs', 'dfs', 'astar', 'mdp-v', 'mdp-p']`

`--fromfile`: local maze file path
```

## Command Examples
I. Generate a new 20*20 maze and use search algorithm to solve it.
```sh
python main.py --rows 20 --cols 20 --solver bfs

python main.py --rows 20 --cols 20 --solver dfs

python main.py --rows 20 --cols 20 --solver astar

python main.py --rows 20 --cols 20 --solver mdp-v

python main.py --rows 20 --cols 20 --solver mdp-p
```