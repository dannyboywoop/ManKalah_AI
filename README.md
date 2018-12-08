
# AI-and-Games-Project-1

Repository for COMP34120:AI and GAMES - Project 1

  

## Manual Requests with Request Handler

Run `GameEngine.py` first:

  ```python GameEngine.py```

Run game engine:

```java -jar ManKalah.jar "nc localhost 12346" "java -jar MKRefAgent.jar"```

The following message should appear on your `GameEngine.py` console:
```
New connection accepted.
Recv: START;South # Raw Message from game engine
START(position=South) # Parsed object
```
Or if you have if the order of the agents is reversed:
```
New connection accepted.
Recv: START;North
START(position=North)
Recv: CHANGE;1;7,7,7,7,7,7,7,0,0,8,8,8,8,8,8,1;YOU
     [ 7][ 7][ 7][ 7][ 7][ 7][ 7]
[ 0]                                 [ 1]
     [ 0][ 8][ 8][ 8][ 8][ 8][ 8]

```

The GameEngine will then proceed to send and recieve moves until the game is over.

## Writing heuristic function

The heuristic function must look like this:

```
def heuristic_function(game_state, player):
        """evaluates value of a GameState to a given player

        Arguments:
        game_state -- GameState instance
        player -- the player index to calculate the value for
        """
    pass
```

## Using command line arguments

You can now specify the port number for the GameEngine to run on, as well as the heuristic function via command line arguments.

To specify only the port number, run `GameEngine.py` with a single argument:

  ```python GameEngine.py 12345```

Otherwise to specify the port number and the heuristic to use, run `GameEngine.py` with a two argument:

  ```python GameEngine.py 12345 TestHeuristics.bad_heuristic```
  
Notice the form of the heuristic function:
==ModuleNameContainingFunction==.==FunctionName==
(It is important to make sure that any modules containing heuristic functions you would like to use are imported by GameEngine).

With the ability to specifiy ports and heuristics through command line arguments, it is now very easy to run two copies of the program against each other with different heuristics (without having to change the source code).

## HeuristicCompTree
The HeuristicCompTree class has been added (along with SharedNode) to make it easier and faster to play to of our bots against each other, with different heuristic functions, to determine a winner. 
Instead of having to run two seperate bots each calculating the game tree and communicating with the server, a single game tree is created and it calculates the best moves for each of the players depending on their heuristic functions.

To get the results of a match between two heuristic functions, simply import `HeuristicCompTree`, instantiate an obect and use the `run_game()` method as follows:

```
HeuristicCompTree(heuristic1, heuristic2).run_game()
```

The method returns a tuple: (heuristic1's score, heuristic2's score).

## C++ Version

You can build the c++ version using the two make files available:
  ```make -f DEBUG.make```
or
  ```make -f release.make```
  
You can clean or rebuild by adding the relevant argument:
  ```make -f DEBUG.make clean```
  
  ```make -f release.make rebuild```
  
By default it runs on port 12346, but you can choose a different port when you run it by adding a single command line argument:


  ```./MankalahAI.out 54123```
  