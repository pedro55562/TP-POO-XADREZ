#map: key : value
ranksTOrows ={
    "1" : 7,
    "2" : 6,
    "3" : 5,
    "4" : 4,
    "5" : 3,
    "6" : 2,
    "7" : 1,
    "8" : 0
}

rowsTOranks ={v : k for k, v in ranksTOrows.items() }

filesTOcols ={
    "h" : 7,
    "g" : 6,
    "f" : 5,
    "e" : 4,
    "d" : 3,
    "c" : 2,
    "b" : 1,
    "a" : 0
}

colsTOfiles ={v : k for k, v in filesTOcols.items() }


defaultFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

WHITEn = 8
BLACKn = 16

EMPTY = 0
KING = 1
QUEEN = 2
ROOK = 3
BISHOP = 4
KNIGHT = 5
PAWN = 6

Type = {
    EMPTY: "EMPTY",
    KING: "KING",
    QUEEN: "QUEEN",
    ROOK: "ROOK",
    BISHOP: "BISHOP",
    KNIGHT: "KNIGHT",
    PAWN: "PAWN"
}

base_path = 'assets/images/chess_pieces/'

Color = {
    WHITEn: "WHITE",
    BLACKn: "BLACK",
}

window_width = 800
window_height = 800
squareSize = 100

dark = (161, 111, 90) 
light = (235, 210, 184, 255)
red_ = (230, 41, 55)
