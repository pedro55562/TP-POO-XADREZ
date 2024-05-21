class Position():
    def __init__(self,Row,Col) -> None:
        self.row = Row
        self.col = Col
        
    def getPosition(self):
        return self
    
    def setPosition(self, Row, Col):
        self.row = Row
        self.col = Col      