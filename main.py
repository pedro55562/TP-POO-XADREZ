
# *****************************************************
# *                                                   *
# * O Lord, Thank you for your goodness in our lives. *
# *     Please bless this code to our compilers.      *
# *                     Amen.                         *
# *                                                   *
# *****************************************************


from src import *

def main():
    fen = "r3k2r/8/8/8/8/8/8/R3K2R w KQkq"
    chessboard = ChessBoard(defaultFen)
    graphicboard = ChessRender(chessboard)

    while graphicboard.getShouldclose() == False:        
        chessboard.printCastlingRights()
        graphicboard.render() 
        graphicboard.setShouldclose()
        graphicboard.render()
        
        chessboard.printMoveLog()
        print("CLEAR:",chessboard.isPathSafe(Position(7,4), Position(7,7)))
        
        if(chessboard.getMoveMade() == True):
            chessboard.setNewValidmoves()
                
        event1 = graphicboard.handle_events()
        
        if event1 == CLOSEGAME:
            break
        elif event1 == UNDOMOVE:
            continue
        elif isinstance(event1, Position):
            start = event1
            graphicboard.updateSelectedPiece(start)
        
        graphicboard.render()
        
        event2 = graphicboard.handle_events()
        
        if event2 == CLOSEGAME:
            break   
        elif event2 == UNDOMOVE:
            continue
        elif isinstance(event2, Position):
            to = event2
            graphicboard.updateSelectedPiece(to)
        
        if (start is not None) and  (to is not None):
            chessboard.movePiece(start, to) 
        
        
    graphicboard.quit()
    print("JOGO FECHADO COM SUCESSO")

if __name__ == "__main__":
    main()