from pwn import *

# Principiante
#
# You have to give the correct answer 12 times in a row with a 1s timeout between each answer.
#
# Base keyboard is :
#
# _____________________________
# |  | | | |  |  | | | | | |  |
# |  | | | |  |  | | | | | |  |
# |  | | | |  |  | | | | | |  |
# |  |_| |_|  |  |_| |_| |_|  |
# |   |   |   |   |   |   |   |
# |   |   |   |   |   |   |   |
# |___|___|___|___|___|___|___|
# Examples of expected answers :
#
# Give me the 4th A# plz
# _________________________________________________________________________________________________________________
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | |X|  |
# |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |
# |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
# |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
# |___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|
#
# Give me the 2nd F plz
# _________________________________________________________
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
# |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |
# |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |
# |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
# |   |   |   |   |   |   |   |   |   |   | X |   |   |   |
# |___|___|___|___|___|___|___|___|___|___|___|___|___|___|
# Connection info: nc prog.dvc.tf 7751
#
# Challenge creator: erovinmo
#
# Noice, here is your flag : dvCTF{4r3_Y0U_7H3_N3X7_M0Z4r7?}

def buildstr(sign):
    lnotes = {
        'C#': "|  |X| | |  |  | | | | | |  |\n",
        'Db': "|  |X| | |  |  | | | | | |  |\n",
        'D#': "|  | | |X|  |  | | | | | |  |\n",
        'Eb': "|  | | |X|  |  | | | | | |  |\n",
        'F#': "|  | | | |  |  |X| | | | |  |\n",
        'Gb': "|  | | | |  |  |X| | | | |  |\n",
        'G#': "|  | | | |  |  | | |X| | |  |\n",
        'Ab': "|  | | | |  |  | | |X| | |  |\n",
        'A#': "|  | | | |  |  | | | | |X|  |\n",
        'Bb': "|  | | | |  |  | | | | |X|  |\n",

    }
    bnotes = {
        'C' : "| X |   |   |   |   |   |   |\n",
        'B#': "| X |   |   |   |   |   |   |\n",
        'D' : "|   | X |   |   |   |   |   |\n",
        'E' : "|   |   | X |   |   |   |   |\n",
        'Fb': "|   |   | X |   |   |   |   |\n",
        'F' : "|   |   |   | X |   |   |   |\n",
        'E#': "|   |   |   | X |   |   |   |\n",
        'G' : "|   |   |   |   | X |   |   |\n",
        'A' : "|   |   |   |   |   | X |   |\n",
        'B' : "|   |   |   |   |   |   | X |\n",
        'Cb': "|   |   |   |   |   |   | X |\n",
    }
    a=[]
    a.append("_____________________________\n")
    a.append("|  | | | |  |  | | | | | |  |\n")
    a.append("|  | | | |  |  | | | | | |  |\n")
    if sign in lnotes:
        a.append(lnotes[sign])
    else:
        a.append("|  | | | |  |  | | | | | |  |\n")
    a.append("|  |_| |_|  |  |_| |_| |_|  |\n")
    a.append("|   |   |   |   |   |   |   |\n")
    if sign in bnotes:
        a.append(bnotes[sign])
    else:
        a.append("|   |   |   |   |   |   |   |\n")
    a.append("|___|___|___|___|___|___|___|\n")
    return a

def process():
    return 1

piano=[
'____________________________',
'|  | | | |  |  | | | | | |  ',
'|  | | | |  |  | | | | | |  ',
'|  | | | |  |  | | | | | |  ',
'|  |_| |_|  |  |_| |_| |_|  ',
'|   |   |   |   |   |   |   ',
'|   |   |   |   |   |   |   ',
'|___|___|___|___|___|___|___',
    ]

r = remote('prog.dvc.tf', 7751)
while(True):
    data=r.recvuntil(b'plz')
    arr=data.split(b'\n')
    print(arr)
    # remove empty line for 2+ iteration
    if arr[0] == b'':
        arr.pop(0)
    result = re.search(r".*\s(\d+)", arr[0].decode("utf-8"))
    try_n = int(result.groups()[0])
    result = re.search(r"Give me the (\d+)\w+\s(\w\#?)\splz", arr[1].decode("utf-8"))
    print(result.groups())
    multiplyer=int(result.groups()[0])-1
    note=str(result.groups()[1])
    note=buildstr(note)
    send_str=''
    for i in range(8):
        send_str += piano[i]*multiplyer
        send_str += note[i]
    print("send string:")
    print(send_str)
    r.send(bytes(send_str, 'UTF-8'))
    print("=========")
    if try_n == 12:
        data = r.recvline()
        data = r.recvline()
        print("Flag:")
        print(data)
        exit()
