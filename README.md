# Multi-Agent project
Multi-Agent pursuit a moving target by speed up cover-set and tie-breaking
## Introduction
This is a research that I am doing as a Master student in University of Tsukuba
In this research, I proposed a method for multi-agent pursuering a single moving target.
Especially this method could be used in real-time video game, such like Pacman or Starwars, Warcraft 
## Real-time
According to pacman rules and player frame rate smooth analysis,
0.1 s moves 1 tile, equally maximum planning time 0.1s one turn
## Grid environment
Currently, up, down, left and right, only four directions movement. 
## Related research
A Cover-Based Approach to Multi-Agent Moving Target Pursuit
## CLI program
	python multiagent.py [map] [algorithm] [agent number] [game number]
Example: 
```python
python multiagent.py basicMap speedupcra 3 10
```
Algorithm: astar, cra (cover-hueristic), speedupcra (speedup cover), abstraction(speedup cra using abstraction)
## Map Abstraction
1. Obstacles 2-dimension array to unconnected graph
2. Unconnected graph to connected graph
3. 2 connected node to a abstracted node (level + 1) 
3. Abstracted graph (level + 1)

## Development environment
- Python 2.7
- Ubuntu 16.04
- Inter Core i7-4790
## Demo
- Round Map (A star algoritm)
![Astar](https://github.com/namidairo777/xiao_multiagent/blob/master/documents/astar.gif)
- Round Map (Proposed method)
![Proposed](https://github.com/namidairo777/xiao_multiagent/blob/master/documents/speedupcra.gif)
- Round Map (Proposed method)
![BigMap](https://github.com/namidairo777/xiao_multiagent/blob/master/documents/bigMap.gif)
# Work to do
1. Abstraction
2. Refinement
3. cover: whole map searching costs too much time
## Project specially thanks to 
Pacman project of Berkeley AI CS188
http://ai.berkeley.edu/home.html
