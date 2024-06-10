class Position():
    def __init__(self,Row,Col) -> None:
        self.__row = Row
        self.__col = Col
        
    def getPosition(self):
        return self
    
    def getRow(self):
        return self.__row    
 
    def getCol(self):
        return self.__col 
    
    def setPosition(self, Row, Col):
        self.__row = Row
        self.__col = Col    
        
    def setPosition(self, pos ):
        self.__row = pos.getRow()
        self.__col = pos.getCol()  