
from .datasize import DataSize

class Offer():
    def __init__(self,aid=-1,id=-1,dataSize=DataSize.ONEKB) -> None:
        self.id = id
        self.aid = aid
        self.dataSize = dataSize
        if self.dataSize == DataSize.ONEKB.name:
            self.data = DataSize.ONEKB
        elif self.dataSize == DataSize.TENKB.name:
            self.data = DataSize.TENKB
        elif self.dataSize == DataSize.HUNDREDKB.name:
            self.data = DataSize.HUNDREDKB
