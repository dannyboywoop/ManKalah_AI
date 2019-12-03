# AI-and-Games-Project-1

Repository for COMP34120:AI and GAMES - Project 1

## Introduction

In this project we have produced an AI bot that can play 7,7 ManKalah. Our main aims were to produce a bot that would make decisions quickly and have a high rate of success when played against other bots.

## Approach

We chose to make our bot perform a MiniMax search with Alpha-Beta pruning to make decisions.
As the game tree for 7,7 ManKalah is very large, it is not feasible to reach the leaf nodes from the root of the tree. As such, beyond a certain depth of search, the values of nodes were approximated using a heuristic function.

This heuristic function was optimised using a genetic algorithm, as is discussed below.

## Heuristic function

We decided to use a heuristic which was a weighted sum of a number of simple heuristics. The base heuristics we used are as follows:

```
H1: Maximise the number of seeds in the players scoring pit
H2: Minimise the number of seeds in opponent’s scoring pit
H3: Maximise player’s go-again moves
H4: Minimise opponent’s go-again moves
H5: Maximise total seeds on player’s side
H6: Minimise total seeds on opponent’s side
H7: Number of empty pits on our side
H8: Number of empty pits on opponent’s side
H9: Minimise player’s vulnerable pits
H10: Maximise opponent’s vulnerable pits
```

The weights assigned to each of these heuristics were decided by running a genetic algorithm that would play heuristics against each other and evolve towards a (hopefully) optimal combination.

## Building the bot

There are two versions of the bot that can be produced, one acts as a TCP server in order to communicate with the game engine and one that is run within the game engine itself, communicating through standard in/out streams.

To build the TCP version use:
  ```make -f TCP.make```

or to build the standalone version use:
  ```make -f standalone.make```
  
You can clean or rebuild by adding the relevant argument:
  ```make -f TCP.make clean```
  
  ```make -f standalone.make rebuild```

## Playing the game

To play the standalone version, run ManKalah.jar with the following argument:
```java -jar ManKalah.jar "other agent" "./Group35AI.out"```

For the standalone version you can add a single command line argument that specifies the maximum depth to search the game tree:
```./Group35AI.out 12```

For the TCP version, you should run this first in a seperate terminal:
```./TCPMankalahAI.out```
before running ManKalah.jar with the following argument:
```java -jar ManKalah.jar "other agent" "nc localhost 12346"```

By default the TCP version runs on port 12346, but you can choose a different port when you run it by adding a single command line argument:
```./TCPMankalahAI.out 54123```
 
You can also enter 10 command line arguments (instead of or after those previously mentioned) that represent the weights you would like to apply to each of the heuristics.

## HeuristicCompTree
The HeuristicCompTree class has been added (along with SharedNode) to make it easier and faster to play two of our bots against each other, with different heuristic functions, to determine a winner. 
Instead of having to run two seperate bots each calculating the game tree and communicating with the engine, a single game tree is created and it calculates the best moves for each of the players depending on their heuristic functions.

## Genetic Algorithm

  
