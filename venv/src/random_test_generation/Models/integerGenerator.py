import random, math, re



class IntTypes:
    INT256 = "INT256"
    INT128 = "INT128"
    INT64 = "INT64"
    INT32 = "INT32"
    INT = "INT"
    UINT256 = "UINT256"
    UINT128 = "UINT128"
    UINT64 = "UINT64"
    UINT32 = "UINT32"
    UINT = "UINT"

 # Define constants
MAX_UINT_256 = (2 ** 256) - 1
MIN_INT_256 = int(- (2 ** 255))
MAX_INT_256 = (2 ** 255) - 1

MAX_UINT_128 = (2 ** 127) - 1
MIN_INT_128 =  int(-(2 ** 127) + 1)
MAX_INT_128 = (2 ** 127) - 1

MAX_UINT_64 = (2 ** 63) - 1
MIN_INT_64 =  int( -(2 ** 63) + 1)
MAX_INT_64 = (2 ** 63) - 1

MAX_UINT_32 = (2 ** 32) - 1
MIN_INT_32 = int(- (2 ** 31) + 1)
MAX_INT_32 = (2 ** 31) - 1

class IntegerGenerator:
   
    global MAX_UINT_256, MIN_INT_256 ,MAX_INT_256 
    global MAX_UINT_128,MIN_INT_128 ,MAX_INT_128 
    global MAX_UINT_64 ,MIN_INT_64 , MAX_INT_64 
    global MAX_UINT_32 ,MIN_INT_32 ,MAX_INT_32 


    def __init__(self):
        self.random = random
        self.highNumber = 1
        self.signedlowNumber = 0
        self.UnsignedlowNumber = 1
        self.randomNumber = 0


    def intGenerator(self, _type):
        _type = _type.upper()

        if _type == IntTypes.INT256 or _type == IntTypes.INT:
            self.highNumber = MAX_INT_256
            self.signedlowNumber = MIN_INT_256

        elif _type == IntTypes.INT128:
            self.highNumber = MAX_INT_128
            self.signedlowNumber = MIN_INT_128

        elif _type == IntTypes.INT64:
            self.highNumber = MAX_INT_64
            self.signedlowNumber = MIN_INT_64

        elif _type == IntTypes.INT32:
            self.highNumber = MAX_INT_32
            self.signedlowNumber = MIN_INT_32

        elif _type == IntTypes.UINT256 or _type == IntTypes.UINT:
            self.highNumber = MAX_UINT_256

        elif _type == IntTypes.UINT128:
            self.highNumber = MAX_UINT_128

        elif _type == IntTypes.UINT64:
            self.highNumber = MAX_UINT_64

        elif _type == IntTypes.UINT32:
            self.highNumber = MAX_UINT_32
            
        else:
            raise ValueError("Invalid integer type specified")

        if _type == IntTypes.UINT or _type.startswith("UINT"):
            self.randomNumber = self.random.randint(self.UnsignedlowNumber, int(self.highNumber))
        else:
            self.randomNumber = int(self.random.uniform(self.signedlowNumber, self.highNumber))

        return str(self.randomNumber)

    def fetch_type(self, type_str):
        integerArr = []
        pattern = r'\[[^\d]*(\d+)[^\d]*\]'
        p = re.compile(pattern, re.MULTILINE)
        _mnum = p.search(type_str)
        blen = 0
        if _mnum:
            match = _mnum.group()
            match = match.replace('[', '')
            match = match.replace(']', '')
            blen = int(match)
            integerArr = [0] * blen
            type_str = type_str[:len(type_str) - (len(match) + 2)]
        else:
            integerArr = [0] * 10
            type_str = type_str[:len(type_str) - 2]
        return integerArr, type_str.upper()

    def intArrGenerator(self, type_str):
        

        integerArr, type_str = self.fetch_type( type_str)

        if type_str in ["INT256","INT"] :
            self.highNumber = MAX_INT_256
            self.signedlowNumber = MIN_INT_256
            for i in range(len(integerArr)):
                self.randomNumber = int(random.random() * ((self.highNumber - self.signedlowNumber) + 1) + self.signedlowNumber)
                integerArr[i] = self.randomNumber

        elif type_str == "INT128":
            self.highNumber = MAX_INT_256
            self.signedlowNumber = MIN_INT_256
            for i in range(len(integerArr)):
                self.randomNumber = int(random.random() * ((self.highNumber - self.signedlowNumber) + 1) + self.signedlowNumber)
                integerArr[i] = self.randomNumber

        elif type_str == "INT64":
            self.highNumber = MAX_INT_64
            self.signedlowNumber = MIN_INT_64
            for i in range(len(integerArr)):
                self.randomNumber = int(random.random() * ((self.highNumber - self.signedlowNumber) + 1) + self.signedlowNumber)
                integerArr[i] = self.randomNumber
        
        elif type_str == "INT32":
            self.highNumber = MAX_INT_32
            self.signedlowNumber = MIN_INT_32
            for i in range(len(integerArr)):
                self.randomNumber = int(random.random() * ((self.highNumber - self.signedlowNumber) + 1) + self.signedlowNumber)
                integerArr[i] = self.randomNumber

        if type_str in ["UINT256","UINT"] :
            self.highNumber = MAX_UINT_256
            self.randomNumber = random.randint(int(self.highNumber) - int(self.UnsignedlowNumber), int(self.highNumber))
            for i in range(len(integerArr)):
                self.randomNumber = int(random.uniform(self.signedlowNumber, self.highNumber+1))
                integerArr[i] = self.randomNumber

        elif type_str == "UINT128":
            self.highNumber = MAX_UINT_128
            self.randomNumber = random.randint(int(self.highNumber) - int(self.UnsignedlowNumber), int(self.highNumber))
            for i in range(len(integerArr)):
                self.randomNumber = int(random.uniform(self.signedlowNumber, self.highNumber+1))
                integerArr[i] = self.randomNumber

        elif type_str == "UINT64":
            self.highNumber = MAX_UINT_64
            self.randomNumber = random.randint(int(self.highNumber) - int(self.UnsignedlowNumber), int(self.highNumber))
            for i in range(len(integerArr)):
                self.randomNumber = int(random.uniform(self.signedlowNumber, self.highNumber+1))
                integerArr[i] = self.randomNumber
        
        elif type_str == "UINT32":
            self.highNumber = MAX_UINT_32
            self.randomNumber = random.randint(int(self.highNumber) - int(self.UnsignedlowNumber), int(self.highNumber))
            for i in range(len(integerArr)):
                self.randomNumber = int(random.uniform(self.signedlowNumber, self.highNumber+1))
                integerArr[i] = self.randomNumber
        
        return integerArr
