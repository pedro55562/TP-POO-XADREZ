class Position():
    def __init__(self,Row,Col) -> None:
        self.row = Row
        self.col = Col
        
    def getPosition(self):
        return self
    
    def getRow(self):
        return self.row    
 
    def getCol(self):
        return self.col 
    
    def setPosition(self, Row, Col):
        self.row = Row
        self.col = Col    
        
    def setPosition(self, pos ):
        self.row = pos.row
        self.col = pos.col  