# Virtuoso

#### medium

You have to give the correct chord name 50 times in a row with a 1s timeout between each answer.

Chords can be minor (m), major, augmented (+) or diminished (-). Since there can be multiple answers, you have to provide an array containing all correct answers.

Keyboard length varies from 3 to 8 single keyboards.

Examples of expected answers :

```
_____________________________________________________________________________________
|  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
|  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
|  | | | |  |  | | | | | |  |  | | | |  |  |X| | | | |  |  | | | |  |  | | | | |X|  |
|  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|   | X |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|
```
Chord ?
['D+', 'F#+', 'A#+']

```
_____________________________________________________________________________________
|  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
|  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
|  | | | |  |  | | | | |X|  |  | | | |  |  | | | | | |  |  |X| | |  |  | | | | | |  |
|  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |   |   | X |   |   |   |   |   |   |   |   |   |
|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|
```
Chord ?
['G-']

Connection info: nc prog.dvc.tf 7753

Difficulty: medium

Challenge creator: erovinmo

Solver: [Script](virtuozzo_solver.py)

flag : dvCTF{Y0U_4r3_7H3_P14N0_M4573r}