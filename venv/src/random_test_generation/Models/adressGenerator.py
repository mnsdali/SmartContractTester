import random
import re

class AddressGenerator:
    def __init__(self, wallet):
        self.wallet = wallet
        
    def addressGenerator(self):
        randomNum = abs(random.randint(0, 100000)) % len(self.wallet)
        return randomNum
    
    def fetch_type(self, type):
        pattern = r"\[[^\d]*(\d+)[^\d]*\]"
        p = re.compile(pattern, re.MULTILINE)
        _mnum = p.search(type)
        if _mnum:
            match = _mnum.group()
            match = match.replace("[", "")
            match = match.replace("]", "")
            blen = int(match)
            adrArr = [None] * blen
            type = type[:type.rindex(match) - 2]
        else:
            adrArr = [None] * len(self.wallet)
            type = type[:-2]
        return adrArr,type

    def addressArrGenerator(self, type):
        adrArr,type= self.fetch_type(type)
        for i in range(len(adrArr)):
            adrArr[i] = self.addressGenerator()

        
    
        
    
    