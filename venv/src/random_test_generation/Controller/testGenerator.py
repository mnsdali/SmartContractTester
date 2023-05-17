from ..Models.adressGenerator import AddressGenerator
from ..Models.booleanGenerator import BooleanGenerator 
from ..Models.byteGenerator import ByteGenerator 
from ..Models.integerGenerator import IntegerGenerator 
from ..Models.stringGenerator import StringGenerator 


class TestGenerator:
    
    def __init__(self, abi, wallet, constructor_inputs) -> None:
        self.abi = abi
        self.wallet = wallet
        self.constructor_inputs = constructor_inputs
        self.byte_gen = ByteGenerator(constructor_inputs)
        self.adress_gen = AddressGenerator(wallet)
        self.bool_gen = BooleanGenerator()
        self.int_gen = IntegerGenerator()
        self.str_gen = StringGenerator()
        self.test_case = []

    
    def fetchQuery(self, query):
        for input in query['inputs']:
            if 'address' in input['type']:
                return self.getAddressGenerator(input['type'])
            elif 'bool' in input['type']:
                return self.getBoolGenerator()
            elif 'bytes' in input['type']:
                return self.getByteGenerator(input['type'])
            elif 'int' in input['type']:
                return self.getIntGenerator(input['type'])
            elif 'string' in input['type']:
                return self.getStringGenerator(input['type']) 
    
    def fetchAbi(self):
        for query in self.abi:
            if query['type'] == 'function':
                if len(query['inputs']) >0:
                    self.test_case.append(self.fetchQuery(query))
        return self.test_case

    def GenerateTestCase(self):
        self.test_case = []
        return self.fetchAbi()

    def getAddressGenerator(self, type):
        if '[' in type:
            addressIndexes = self.adress_gen.addressArrGenerator(input['type'])
            for i in range(len(addressIndexes)):
                addressIndexes[i] = 'accounts[{addressIndexes[i]}]'
            return addressIndexes
        
        else:
            addressIndex = self.adress_gen.addressGenerator()
            return addressIndex
    
    def getBoolGenerator(self):
        return self.bool_gen.boolGenerator()
        
    
    def getByteGenerator(self, type):
        if '[' in type:
            bytesTokens = self.str_gen.stringArrGenerator(type)
            for s in bytesTokens:
                s = s.strip().encode('utf-8')
                s =  f'{s}'
            return bytesTokens
        else:
            s = self.byte_gen.byteGenerator().strip().encode('utf-8')
            s =  f'{s}'
            return s
    
    def getIntGenerator(self, type):
        if '[' in type:
            return self.int_gen.intArrGenerator(type)
        else:
            return self.int_gen.intGenerator(type)
    
    def getStringGenerator(self, type):
        if '[' in type:
            return self.str_gen.stringArrGenerator(type)
        else:
            return self.str_gen.stringGenerator()

    


    