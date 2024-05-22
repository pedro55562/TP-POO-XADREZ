#
# *****************************************************
# *                                                   *
# * O Lord, Thank you for your goodness in our lives. *
# *     Please bless this code to our compilers.      *
# *                     Amen.                         *
# *                                                   *
# *****************************************************
#

from src import *

fen = "K6N/2p5/8/8/r1bk4/8/5p2/Q6n"
chessboard = ChessBoard(fen)
chessboard.printBoard()
graphicboard = ChessRender(chessboard)

while graphicboard.getShouldclose() == False:
    graphicboard.setShouldclose()
    graphicboard.render()
    pos = graphicboard.HandleMouseInput()
    if pos == -1:
        break
    print(pos.getRow()," ",pos.getCol())
    
graphicboard.quit()
print("JOGO FECHADO COM SUCESSO")
