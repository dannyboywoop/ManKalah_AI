
# AI-and-Games-Project-1

Repository for COMP34120:AI and GAMES - Project 1

  

## Manual Requests with Request Handler

Run `RequestHandler.py` first:

  ```python RequestHandler.py```

Run game engine:

```java -jar ManKalah.jar "nc localhost 12346" "java -jar MKRefAgent.jar"```

The following message should appear on your `RequestHandler.py` console:
```
New connection accepted.
Recv: START;South # Raw Message from game engine
START(position=South) # Parsed object
```
Currently, you cannot respond to this. To view a state, you will need to go second.

```java -jar ManKalah.jar "java -jar MKRefAgent.jar" "nc localhost 12346"```

Which should give you the following output:
```
New connection accepted.
Recv: START;North
START(position=North)
Recv: CHANGE;1;7,7,7,7,7,7,7,0,0,8,8,8,8,8,8,1;YOU
     [ 7][ 7][ 7][ 7][ 7][ 7][ 7]
[ 0]                                 [ 1]
     [ 0][ 8][ 8][ 8][ 8][ 8][ 8]

```