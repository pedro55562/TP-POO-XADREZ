
# *****************************************************
# *                                                   *
# * O Lord, Thank you for your goodness in our lives. *
# *     Please bless this code to our compilers.      *
# *                     Amen.                         *
# *                                                   *
# *****************************************************


from src import *
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq"
chessboard = ChessBoard(fen)
graphicboard = ChessRender(chessboard)

while graphicboard.getShouldclose() == False:
    graphicboard.setShouldclose()
    graphicboard.render()
    
    chessboard.printMoveLog()
    chessboard.printCastlingRights()
    
    
    if(chessboard.getMoveMade() == True):
        chessboard.setNewValidmoves()
            
    from_ = graphicboard.HandleMouseInput()
    
    
    # tirar essa gambiarra
    # referente a parte interna de diferentes valores de retorno em HandleMouseInput
    # para diferentes tipos de eventos
    # talvez tranformar handlemouseinput em um lidador de eventos em gerais!
    if from_ == -1:
        break
    elif from_ ==-2:
        continue
    
    graphicboard.updateSelectedPiece(from_)
    
    graphicboard.render()
    
    to = graphicboard.HandleMouseInput()
    
    if to == -1:
        break   
    elif from_ == -2:
        continue
    
    graphicboard.updateSelectedPiece(from_)
    

    chessboard.movePiece(from_, to) 
    
    
graphicboard.quit()
print("JOGO FECHADO COM SUCESSO")
