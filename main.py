
# *****************************************************
# *                                                   *
# * O Lord, Thank you for your goodness in our lives. *
# *     Please bless this code to our compilers.      *
# *                     Amen.                         *
# *                                                   *
# *****************************************************


from src import *

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def getChoice(end : int) -> int :
    k = input("Digite sua opção: ")
    if(k.isnumeric() == False):
        return -1
    if is_integer(k) == False:
        return -1
    else:
        k = int(k)
        if(0 <= k <= end):
            return k
        
    return -1

def game()-> int:
    chessboard = ChessBoard(defaultFen)
    graphicboard = ChessRender(chessboard)

    while graphicboard.getShouldclose() == False:  
        if(chessboard.getMoveMade() == True):
            chessboard.setNewValidmoves()
              
        print(f"\n\n {chessboard.checkMate} \n\n") 
        if(chessboard.checkMate):
            if( chessboard.isWhiteTurn):
                graphicboard.quit()
                return 2 #vitoria das pretas
            else:
                graphicboard.quit()
                return 1 #vitoria das brancas
        
        if(chessboard.stalteMate):
            graphicboard.quit()
            return 3 #empate
           
        graphicboard.render() 
        graphicboard.setShouldclose()
        graphicboard.render()
        
        chessboard.printMoveLog()
                
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
    
      
def createAccount(gm : GameManagement):
    while True:
        print("--------------------------------------------------")
        print("Criando a conta")
        print("--------------------------------------------------")
        name = input("Digite o nome da conta: ")
        p1 = input("Crie uma senha: ")
        print("--------------------------------------------------")
        acount = gm.addUser(name, p1)
        if acount:
            print("Conta criada com sucesso.")
            print("--------------------------------------------------")
            break
        else:
            print("Nome já existente. Deseja tentar novamente?")
            choice = getChoice(1)
            if choice == 0:
                break

def accessAccount(gm : GameManagement):
    while True:
        print("--------------------------------------------------")
        print("Acessando a conta")
        print("--------------------------------------------------")
        name = input("Digite o nome da sua conta: ")
        password = input("Digite sua senha: ")
        print("--------------------------------------------------")
        user = gm.createUser(name, password)
        if user:
            accountMenu(gm, user)
            break
        else:
            print("Informações incorretas! Deseja tentar novamente?")
            print("Não [0]")
            print("Sim [1]")
            choice = getChoice(1)
            if choice == 0:
                break

def accountMenu(gm : GameManagement, user : User):
    while True:
        print("--------------------------------------------------")
        print(f"\tSeja bem-vindo {user.name}!")
        print("O que você gostaria de fazer?")
        print("--------------------------------------------------")
        print("Ver histórico [0]")
        print("Sair da conta [1]")
        
        choice = getChoice(1)
        if choice == 0:
            print("--------------------------------------------------")
            print("\t Histórico: ")
            print("--------------------------------------------------")
            gm.printUserHistory(user)
            print("--------------------------------------------------")
        elif choice == 1:
            break
        else:
            print("Opção inválida, tente novamente.")

def loginUserForGame(gm : GameManagement , color : str):
    while True:
        print(f"Acessando a conta das peças {color}!")
        print("--------------------------------------------------")
        name = input("Digite o nome da sua conta: ")
        password = input("Digite sua senha: ")
        print("--------------------------------------------------")
        user = gm.createUser(name , password)
        if user:
            print(f"O jogador {name} jogará com as peças {color}.")
            return user
        else:
            print("Informações incorretas! Deseja tentar novamente?")
            print("Não [0]")
            print("Sim [1]")
            choice = getChoice(1)
            if choice == 0:
                return None

def startGame(gm : GameManagement):
    print("--------------------------------------------------")
    print("Iniciando a partida!")
    print("--------------------------------------------------")
    white_user = loginUserForGame(gm, 'brancas')
    if not white_user:
        return

    black_user = loginUserForGame(gm, 'pretas')
    if not black_user:
        return
    
    # Aqui você chamaria a função que inicia o jogo de xadrez e determina o vencedor
    # Substitua a chamada de game() pela sua implementação de jogo de xadrez
    winner_is_white = game()
    
    gm.addGame(white_user, black_user, "FEN_final_aqui", winner_is_white)
    print("Partida registrada com sucesso.")

def main():
    gm = GameManagement()
    
    while True:
        print("--------------------------------------------------")
        print("\t Bem-vindo ao jogo de xadrez!")
        print("\t Você está no menu principal.")
        print(" O que deseja fazer? ")
        print("--------------------------------------------------")
        print("Iniciar uma partida com histórico [0]")
        print("Acessar minha conta [1]")
        print("Criar conta [2]")
        print("Fechar jogo [3]")
        print("--------------------------------------------------")
        choice = getChoice(3)
        print("--------------------------------------------------")
        if choice == -1:
            print("Opção inválida.")
        elif choice == 0:
            startGame(gm)
        elif choice == 1:
            accessAccount(gm)
        elif choice == 2:
            createAccount(gm)
        elif choice == 3:
            print("JOGO FECHADO")
            break
                    
if __name__ == "__main__":
    main()