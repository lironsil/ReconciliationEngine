import datetime as dt
from datetime import datetime

class Payable(object):
    """description of class"""
    def __init__(self, id,referencedId,amount,dateOccured):
        self.id=id
        self.referencedId=referencedId
        self.amount=amount
        self.dateOccured=dateOccured

        

