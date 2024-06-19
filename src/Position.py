class Position():
    '''
    :param row: A linha da posicao 
    :param col: A coluna da posicao
    '''    
    def __init__(self, Row : int, Col : int) -> None:
        self.__row = Row
        self.__col = Col

    '''
    :return: A propria posicao
    '''           
    def getPosition(self) -> int:
        return self
    
    '''
    :return: A linha da posicao
    '''        
    def getRow(self) -> int:
        return self.__row    
    
    '''
    :return: A coluna da posicao
    '''     
    def getCol(self) -> int:
        return self.__col 
    
    '''
    :param row: A linha da posicao
    :param col: A coluna da posicao
    '''    
    def setPosition(self, Row : int , Col : int) -> None:
        self.__row = Row
        self.__col = Col    
    
    '''
    :param pos: Uma posicao 
    '''    
    def setPosition(self, pos) -> None:
        self.__row = pos.getRow()
        self.__col = pos.getCol()  