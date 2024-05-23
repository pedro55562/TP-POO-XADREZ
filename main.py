#
# *****************************************************
# *                                                   *
# * O Lord, Thank you for your goodness in our lives. *
# *     Please bless this code to our compilers.      *
# *                     Amen.                         *
# *                                                   *
# *****************************************************


from src import *
fen = "8/2k5/8/8/8/8/2K5/8"
chessboard = ChessBoard(defaultFen)
graphicboard = ChessRender(chessboard)

while graphicboard.getShouldclose() == False:
    graphicboard.setShouldclose()
    graphicboard.render()

    chessboard.printBoard()
    
    if(chessboard.getMoveMade() == True):
        chessboard.setNewValidmoves()
            
    
    from_ = graphicboard.HandleMouseInput()
    
    if from_ == -1:
        break
    elif from_ ==-2:
        continue
    
    graphicboard.updateSelectedPiece(from_)
    
    graphicboard.render()
    print( graphicboard.getSelectedPiecePos().getRow()," ", graphicboard.getSelectedPiecePos().getCol())
    
    to = graphicboard.HandleMouseInput()
    
    if to == -1:
        break   
    elif from_ == -2:
        continue
    
    graphicboard.updateSelectedPiece(from_)
    
    chessboard.movePiece(from_, to)
    
    
graphicboard.quit()
print("JOGO FECHADO COM SUCESSO")
