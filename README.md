# tetromino
A SAT based tetromino solver.

This solver is far less generic than the one of [cemulate](https://github.com/cemulate/polyomino-solver), but enough to solve all tetromino puzzles in the [Talos principle](http://www.croteam.com/talosprinciple/).

**Dependency:** [satispy](https://github.com/netom/satispy)

**Usage:** `$ python tetromino_sat.py nrow ncol shapes`, where `nrow` and `ncol` are the number of rows and columns of the table to fill with tetromino and `shapes` should be the list of the shape identifiers of the tetromino pieces of the problem, separated by a comma.

**Shape identifiers:**

![](https://vignette.wikia.nocookie.net/tetrisconcept/images/c/ca/Tetromino_image.png/revision/latest/scale-to-width-down/340?cb=20090706171943)

1. cyan
2. yellow
3. orange
4. blue
5. green
6. red
7. purple

* Example 1 : python tetromino_sat.py 4 4 1,2,3,4

| 1 | 1 | 1 | 1 |
|---|---|---|---|
| 3 | 2 | 2 | 4 |
| 3 | 2 | 2 | 4 |
| 3 | 3 | 4 | 4 |

* Example 2 (waken the 2nd messenger in the Talos Principle game) : tetromino_sat.py 6 8 1,7,7,2,2,5,6,6,6,4,4,4

| 1 | 1 | 1 | 1 | 4 | 4 | 5 | 5 |
|---|---|---|---|---|---|---|---|
| 2 | 2 | 2 | 2 | 4 | 5 | 5 | 6 |
| 2 | 2 | 2 | 2 | 4 | 6 | 6 | 6 |
| 4 | 4 | 6 | 4 | 6 | 6 | 6 | 7 |
| 4 | 6 | 6 | 4 | 6 | 7 | 7 | 7 |
| 4 | 6 | 4 | 4 | 7 | 7 | 7 | 7 |
