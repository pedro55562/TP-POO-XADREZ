import hashlib
import json
import os

class User:
    def __init__(self, name: str, passwordHash: str) -> None:
        self.name = name
        self.passwordHash = passwordHash
        
    def __eq__(self, value) -> bool:
        if isinstance(value, User):
            return (value.name == self.name)
        return False
    
class UserAdmin(User):
    def __init__(self, name, passwordHash) -> None:
        super().__init__(name, passwordHash)
        self.admin = True

class GameManagement:
    def __init__(self) -> None:
        self.users = []
        self.__load_users_from_file('data/users.json')
        self.logeduser = None
        
    def __load_users_from_file(self, filename: str):
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as file:
                    users_data = json.load(file)
                    for user_data in users_data:
                        if user_data.get('admin', False):
                            user = UserAdmin(user_data['name'], user_data['passwordHash'])
                        else:
                            user = User(user_data['name'], user_data['passwordHash'])
                        self.users.append(user)
            except json.JSONDecodeError:
                print(f"Erro ao ler o arquivo {filename}. O arquivo pode estar vazio ou corrompido.")
                self.users = []
    
    def __save_users_to_file(self, filename: str):
        users_data = []
        for user in self.users:
            user_data = {
                'name': user.name,
                'passwordHash': user.passwordHash
            }
            if isinstance(user, UserAdmin):
                user_data['admin'] = True
            users_data.append(user_data)
        
        with open(filename, 'w') as file:
            json.dump(users_data, file, indent=4)
    
    def logIn(self, name: str, password: str) -> int:
        for user in self.users:
            if user.name == name and self.verify_password(password, user):
                self.logeduser = user
                return 0
        return -1
    
    def __getHashfromPassword(self, password: str) -> str:
        # Usando SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    
    def verify_password(self, password: str, user: User) -> bool:
        return self.__getHashfromPassword(password) == user.passwordHash

    def addUser(self, name: str, password: str, isAdmin: bool = False) -> bool:
        passwordHash = self.__getHashfromPassword(password)
        
        if len(self.users) != 0:
            temp = User(name, passwordHash)
            for user in self.users:
                if temp == user:
                    return False
        
        if isAdmin:
            new_user = UserAdmin(name, passwordHash)
        else:
            new_user = User(name, passwordHash)
        self.users.append(new_user)
        self.__save_users_to_file('data/users.json')
        self.__create_user_json(name)
        return True

    def printUserHistory(self, user: User):
        filename = f'data/{user.name}_games.json'
        
        if not os.path.exists(filename):
            print(f"Arquivo JSON do jogador {user.name} não encontrado.")
            return False
        
        with open(filename, 'r') as file:
            user_data = json.load(file)
        
        for game in user_data['games']:
            print(f"Oponente: {game['opponent']}\nResultado: {game['result']}\n")
        return True
        
    def __create_user_json(self, username: str):
        filename = f'data/{username}_games.json'
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                user_data = {
                    "player_name": username,
                    "games": []
                }
                json.dump(user_data, file, indent=4)
                    
                
    def validUser(self, name : str , password : str) -> bool:
        if len(self.users) != 0:
            user = User(name, self.__getHashfromPassword(password))
            for user in self.users:
                if user == user:
                    return True
                
                        
    def createUser(self, name: str, password: str, isAdmin: bool = False) -> User:
        passwordHash = self.__getHashfromPassword(password)
        if isAdmin:
            return UserAdmin(name, passwordHash)
        else:
            return User(name, passwordHash)

    def createAcount(self, name: str , password : str) -> int:
        passwordHash = self.__getHashfromPassword(password)
        if len(self.users) != 0:
            temp = User(name, passwordHash)
            for user in self.users:
                if temp == user:
                    return 1    #nome invalido
        
        if self.__isPasswordValid(password) == False:
            return 2 #senha invalida
        
        self.addUser(name, password)
        return 0 # conta criada com sucesso
        
    def addGame(self, whiteuser: User, blackuser: User, fen: str, result: int):
        whiteresult = -1
        blackresult = -1
        if(result == 2):
            whiteresult = "derrota"
            blackresult = "vitoria"
        if(result == 1):
            whiteresult = "vitoria"
            blackresult = "derrota"         
        if(result == 3):
            whiteresult = "empate"
            blackresult = "empate"        
  
        white_filename = f'data/{whiteuser.name}_games.json'
        black_filename = f'data/{blackuser.name}_games.json'
        
        # Verificar se os arquivos JSON dos jogadores existem
        if not os.path.exists(white_filename):
            print(f"Arquivo JSON do jogador branco {whiteuser.name} não encontrado.")
            return False
        
        if not os.path.exists(black_filename):
            print(f"Arquivo JSON do jogador preto {blackuser.name} não encontrado.")
            return False
        
        # Carregar dados do jogador branco
        with open(white_filename, 'r') as white_file:
            white_data = json.load(white_file)
        
        # Adicionar nova partida ao jogador branco
        white_data['games'].append({
            "opponent": blackuser.name,
            "result": whiteresult,
        })
        
        # Salvar dados do jogador branco de volta ao arquivo JSON
        with open(white_filename, 'w') as white_file:
            json.dump(white_data, white_file, indent=4)
        
        # Carregar dados do jogador preto
        with open(black_filename, 'r') as black_file:
            black_data = json.load(black_file)
        
        # Adicionar nova partida ao jogador preto
        black_data['games'].append({
            "opponent": whiteuser.name,
            "result": blackresult,
        })
        
        # Salvar dados do jogador preto de volta ao arquivo JSON
        with open(black_filename, 'w') as black_file:
            json.dump(black_data, black_file, indent=4)
        
        print("Nova partida adicionada com sucesso para ambos os jogadores.")
        return True
        
        
    def __isPasswordValid(self, password : str):
        return True
    
def main():
    gm = GameManagement()
    
    gm.addUser("pedro","batata")
    
    # Mostrar todos os usuários
    print("\nLista de usuários:")
    for user in gm.users:
        role = "Admin" if isinstance(user, UserAdmin) else "User"
        print(f"Nome: {user.name}, Papel: {role}")

