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

chessboard = ChessBoard(defaultFen)
graphicboard = ChessRender(chessboard)

while graphicboard.getShouldclose() == False:
    chessboard.printBoard()
    graphicboard.setShouldclose()
    graphicboard.render()
    
    from_ = graphicboard.HandleMouseInput()
    if from_ == -1:
        break
    
    graphicboard.updateSelectedPiece(from_)
    
    graphicboard.render()
    print( graphicboard.getSelectedPiecePos().getRow()," ", graphicboard.getSelectedPiecePos().getCol())
    
    to = graphicboard.HandleMouseInput()
    if to == -1:
        break   
    
    graphicboard.updateSelectedPiece(from_)
    
    chessboard.movePiece(from_, to)
    
            
graphicboard.quit()
print("JOGO FECHADO COM SUCESSO")