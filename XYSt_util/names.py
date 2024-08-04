from enum import IntEnum

class Names(IntEnum):
    WHITE=0 #player
    BLACK=1 #bot

class Space(IntEnum):
    WHITE=-1 #player
    BLACK=1 #bot
    EMPTY=0 #empty space