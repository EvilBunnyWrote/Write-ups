from pwn import *
from pychord import find_chords_from_notes
import itertools

# Confermato(medium)
#
# You have to give the correct chord name 50 times in a row with a 1s timeout between each answer.
#
# Chords can be minor (m) or major.
#
# Keyboard length is constant.
#
# Examples of expected answers :
#
# _________________________________________________________
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
# |  | | | |  |  | | |X| | |  |  | | | |  |  | | | | | |  |
# |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |
# |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
# | X |   |   |   |   |   |   |   |   |   | X |   |   |   |
# |___|___|___|___|___|___|___|___|___|___|___|___|___|___|
#
# Chord ?
# Fm
#
# _________________________________________________________
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
# |  | | |X|  |  | | | | | |  |  | | | |  |  | | |X| | |  |
# |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |
# |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
# | X |   |   |   |   |   |   |   |   |   |   |   |   |   |
# |___|___|___|___|___|___|___|___|___|___|___|___|___|___|
#
# Chord ?
# G#
# Connection info: nc prog.dvc.tf 7752
#
# Challenge creator: erovinmo
#
# You win ! Here is your flag : dvCTF{CH0P1N_W0U1D_H4V3_833N_Pr0UD}

r = remote('prog.dvc.tf', 7752)
while(True):
    data = r.recvuntil(b'Chord ?')
    arr = data.split(b'\n')
    print(arr)
    result = re.search(r".*\s(\d+)", arr[0].decode("utf-8") )
    n_round = result.groups()[0]
    print(f"Round {n_round}")
    blacks = [pos for pos, char in enumerate(arr[4].decode("utf-8")) if char == 'X']
    whites = [pos for pos, char in enumerate(arr[7].decode("utf-8")) if char == 'X']
    print(f"Whites as pos {whites}, blacks at {blacks}")
    # White keys positions
    w_notes = {
        2:  'C',
        6:  'D',
        10: 'E',
        14: 'F',
        18: 'G',
        22: 'A',
        26: 'B',
        30: 'C',
        34: 'D',
        38: 'E',
        42: 'F',
        46: 'G',
        50: 'A',
        54: 'B',
    }
    # Black keys positions
    b_notes = {
        4:  'C#',
        8:  'D#',
        16: 'F#',
        20: 'G#',
        24: 'A#',
        32: 'C#',
        36: 'D#',
        44: 'F#',
        48: 'G#',
        52: 'A#',
    }
    chord_notes = []
    for pos in whites:
        chord_notes.append(w_notes[pos])
    for pos in blacks:
        chord_notes.append(b_notes[pos])
    print(f"Chord notes are {chord_notes}")
    perms = list(itertools.permutations(chord_notes))
    for perm in perms:
        res = find_chords_from_notes(perm)
        if not res:
            continue
        else:
            print(f"Chord is {res}")
            res_chord = ((res[0].info().split("\n"))[0].split("/"))[0]
            print(f"Send {res_chord}")
            r.send(bytes(res_chord,'UTF-8')+b'\n')
            data = r.recvline()
            print(data)
            break

    if int(n_round) == 50:
        data = r.recvline()
        print("Flag:")
        print(data)
        exit()
