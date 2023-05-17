import re
import random

class StringGenerator:
    def __init__(self, hex_down=65, hex_up=122):
        self.hex_down = hex_down # letter 'A'
        self.hex_up = hex_up # letter 'z'
        self.random = random
    
    def fetch_type(self, type):
        pattern = r"\[[^\d]*(\d+)[^\d]*\]"
        p = re.compile(pattern, re.MULTILINE)
        _mnum = p.search(type)
        if _mnum:
            match = _mnum.group()
            match = match.replace("[", "")
            match = match.replace("]", "")
            blen = int(match)
            strArr = [None] * blen
            type = type[:type.rindex(match) - 2]
        else:
            strArr = [None] * 10
            type = type[:-2]
        return strArr, type

    def stringGenerator(self):
        buffer = []
        targetStringLength = self.random(1000)+1
        for i in range(targetStringLength):
            randomLimitedInt = self.hex_down + int(self.random.random() * (self.hex_up - self.hex_down + 1))
            buffer.append(chr(randomLimitedInt))
        return ''.join(buffer)

    

    def stringArrGenerator(self, type):
        strArr, type = self.fetch_type(type)
        for i in range(len(strArr)):
            buffer = []
            targetStringLength = self.random(1000)+1
            for k in range(targetStringLength):
                randomLimitedInt = self.hex_down + int(self.random.random() * (self.hex_up - self.hex_down + 1))
                buffer.append(chr(randomLimitedInt))
            strArr[i] = ''.join(buffer)
        
        return strArr

