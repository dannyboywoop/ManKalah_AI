
# AI-and-Games-Project-1

Repository for COMP34120:AI and GAMES - Project 1

  

## Manual Requests with Request Handler

Run `RequestHandler.py` first:

  ```python RequestHandler.py```

Run game engine:

```java -jar ManKalah.jar "nc localhost 12346" "java -jar MKRefAgent.jar"```

The following message should appear on your `RequestHandler.py` console:
```
Recv: b'START;South' # Raw Message from game engine
START(position=South) # Parsed object
```
You can now type out responses and press enter, for example:

```
MOVE;1 # My response
Recv: b'CHANGE;1;7,7,7,7,7,7,7,0,0,8,8,8,8,8,8,1;OPP' # Raw change message
CHANGE (moveswap=1, state=7,7,7,7,7,7,7,0,0,8,8,8,8,8,8,1, turn=OPP) # parsed object
```