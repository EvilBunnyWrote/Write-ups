from pwn import *
from pychord import find_chords_from_notes
import itertools

# Virtuoso
#
# medium
# You have to give the correct chord name 50 times in a row with a 1s timeout between each answer.
#
# Chords can be minor (m), major, augmented (+) or diminished (-). Since there can be multiple answers, you have to provide an array containing all correct answers.
#
# Keyboard length varies from 3 to 8 single keyboards.
#
# Examples of expected answers :
#
# _____________________________________________________________________________________
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
# |  | | | |  |  | | | | | |  |  | | | |  |  |X| | | | |  |  | | | |  |  | | | | |X|  |
# |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |
# |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
# |   | X |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
# |___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|
#
# Chord ?
# ['D+', 'F#+', 'A#+']
#
# _____________________________________________________________________________________
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
# |  | | | |  |  | | | | |X|  |  | | | |  |  | | | | | |  |  |X| | |  |  | | | | | |  |
# |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |
# |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
# |   |   |   |   |   |   |   |   |   |   |   | X |   |   |   |   |   |   |   |   |   |
# |___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|
#
# Chord ?
# ['G-']
# Connection info: nc prog.dvc.tf 7753
#
# Difficulty: medium
# Challenge creator: erovinmo

#You win ! Here is your flag : dvCTF{Y0U_4r3_7H3_P14N0_M4573r}

r = remote('prog.dvc.tf', 7753)
while(True):
    data = r.recvuntil(b'Chord ?')
    arr = data.split(b'\n')
    print(arr)
    result = re.search(r".*\s(\d+)",arr[0].decode("utf-8") )
    round=result.groups()[0]
    print(f"Round {round}")
    blacks = [pos for pos, char in enumerate(arr[4].decode("utf-8")) if char == 'X']
    whites = [pos for pos, char in enumerate(arr[7].decode("utf-8")) if char == 'X']
    print(f"Whites as pos {whites}, blacks at {blacks}")
    w_notes={
        2: 'C',
        6: 'D',
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
    b_notes={
        4:'C#',
        8: 'D#',
        16: 'F#',
        20: 'G#',
        24: 'A#',
        32: 'C#',
        36: 'D#',
        44: 'F#',
        48: 'G#',
        52: 'A#',
    }
    chord_notes=[]
    for pos in whites:
        chord_notes.append(w_notes[pos%56])
    for pos in blacks:
        chord_notes.append(b_notes[pos%56])
    print(f"Chord notes are {chord_notes}")
    perms=list(itertools.permutations(chord_notes))
    for perm in perms:
        res = find_chords_from_notes(perm)
        if res == []:
            continue
        else:
            print(f"Chord is {res}")
            res_chord_array=[]
            for chord in res:
                res_chord=((chord.info().split("\n"))[0].split("/"))[0]
                res_chord=res_chord.replace('aug',"+")
                res_chord=res_chord.replace('dim', "-")
                res_chord_array.append(res_chord)
            res_chord_array_str="['"+"', '".join(res_chord_array)+"']"
            print(f"Send {bytes(res_chord_array_str,'UTF-8')}")
            r.send(bytes(res_chord_array_str,'UTF-8')+b'\n')
            data = r.recvline()
            print(data)
            break
            
    if int(round)==50:
        data = r.recvline()
        print("Flag:")
        print(data)
        exit(1)