# Snake Game
I made the snake game.  Very original, no one has ever done this before.
Wow.


Yeah, ok so this isn't original.  I made the game using
[this tutorial](https://pythonspot.com/snake-with-pygame/).
I changed it signifcantly so that I could hack my bot into it
to play it for me.

### BFS Shortest Path
Every time I get an apple, I do a BFS to find the shortest path to the next apple.
I just keep doing that until it is no longer possible.


### Pitfalls
This solution is decent, but far from perfect.  When playing the game,
there is some deliberate zig-zagging done to be sure that you never get into a
position where you are cutting yourself off.

My solution doesn't GAF about zig-zagging.  It just wants to get the the apple ASAP.
So, it is apt to cut itself off.  Oh well.


### Next
Try neural net?  Will it be smarter than BFS?  Probably, if someone who
was good at ML did it.  I don't know much ML, so mine will probably just
run in circles for a while.
