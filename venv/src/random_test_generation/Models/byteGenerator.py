import re
import secrets, random
import string

class ByteGenerator:

    def __init__(self, construct_inputs):
        self.constructor_inputs = construct_inputs
        self._bytes = self.getBytesFromConstructorAndGenerateOthers()
    
    def is_bytes32(self, variable_to_check):
        return type(variable_to_check) is bytes and len(variable_to_check) == 32


        
    def generate_random_string(self, length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))
    
    def getBytesFromConstructorAndGenerateOthers(self):
        _bytes = []
        for input in self.constructor_inputs:
            if self.is_bytes32(input):
                _bytes.append(input)
        
        for _ in range(random.randint(5, 10)):
            _bytes.append(self.generate_random_string(random.randint(5,10)))
        return _bytes
        

    def byteGenerator(self):
        return random.choice(self._bytes)

   
        
    def byteArrGenerator(self, _type):
        leftBracket = _type.find('[')
        rightBracket = _type.find(']') # [12] , 3 - 0 -1 = 2
        if rightBracket - leftBracket > 1:
            blen = int(_type[leftBracket:rightBracket])
            bytes = [''] * blen
            _type = _type[:leftBracket]
        else:
            bytes = [''] * random.randint(1,10)
        try:
            for i in range(len(bytes)):
                bytes[i] = random.choice(self._bytes)

        except Exception as e:
            raise e
        
        return bytes