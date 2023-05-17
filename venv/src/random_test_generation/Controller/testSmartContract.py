
from .testGenerator import TestGenerator
from ..Models.adressGenerator import AddressGenerator
from ..Models.etherGenerator import EtherGenerator

class TestSmartContract:
    
    def __init__(self, abi , wallet, contract_name, contract_instance, constructor_inputs) -> None:
        self.abi = abi 
        self.wallet = wallet
        self.contract_instance = contract_instance
        self.constructor_inputs = constructor_inputs
        self.test_generator = TestGenerator(abi, wallet, constructor_inputs)
        self.contract_name = contract_name
        self.adress_gen = AddressGenerator(wallet)
        self.eth_gen = EtherGenerator()

    def addFailAssertion(self):
        return 'assert False, "Not yet implemented"'
    
    def generateTestCase(self):
        return self.test_generator.GenerateTestCase()


    def add_to_testTemplate(self, query, test_case, id, account, amount):
    
        _function = "\n\ndef test_"+ query['name']+'('
        if self.isPayable(query['stateMutability']):
            tmpFunction, id = self.treatPayable(query, test_case, id, account, amount)
            _function += tmpFunction  

        elif self.isNonPayable(query['stateMutability']):
            tmpFunction, id = self.treatNonPayable(query, test_case, id, account)
            _function += tmpFunction 

        elif self.isView(query['stateMutability']):
            tmpFunction, id = self.treatView(query, test_case, id)
            _function += tmpFunction 
        

    
        return _function, id
    
    def generateInstance(self):
        contract_name = self.contract_name.lower()
        constructor_inputs = list(map(lambda s : str(s), self.constructor_inputs))
        constructor_inputs_str = ','.join(constructor_inputs)
        instance = f'\n\n@pytest.fixture\ndef {contract_name}():\n\t'.expandtabs(4)
        instance += f'return accounts[0].deploy({self.contract_name}, {constructor_inputs_str})'
        return instance

    # transfer(accountDest )
    def generateTestFileTemplate(self):
        acc = self.adress_gen.addressGenerator()
        amount = self.eth_gen.ethGenerator()
        test_case_inputs = self.generateTestCase()
        full_test_case = {'inputs': test_case_inputs, 'account': acc, 'amount': amount}
        id = 0

        test_template= "import pytest\n"
        test_template+= f"from brownie import {self.contract_name}, accounts"
        test_template+= self.generateInstance()
        for query in self.abi:
            if query['type']=='function':
                _function, id = self.add_to_testTemplate(query, test_case_inputs , id, acc, amount)
                test_template += _function
        
        return test_template, full_test_case

    def isPayable(self, sttMut):
        return sttMut == 'payable'
    
    def isView(self, sttMut):
        return sttMut == 'view' or sttMut =='pure'

    def isNonPayable(self, sttMut):
        return sttMut == 'nonpayable'
    
    # contractInstance.contractFunction(*inputs, {"from" : account[x], "amount": random})
    def treatPayable(self, query, test_case, id, account, amount):
        contract_name = self.contract_name.lower()
        _function= self.contract_name.lower()
        _function+= ', accounts): \n\t'.expandtabs(4)
        _function+= f'{contract_name}.'+ query['name'] + '('
        for input in query['inputs']:
            _function+= f'{str(test_case[id])}, '
            id+=1
        
        _function+= '{"from": '+ f'accounts[{account}]' + ', "amount": ' + str(amount) + '})\n\t'.expandtabs(4)
        _function += self.addFailAssertion()
        return _function, id
    
    # contractInstance.contractFunction(*inputs, {"from" : account[x]})
    def treatNonPayable(self, query, test_case, id, account):
        contract_name = self.contract_name.lower()
        _function= self.contract_name.lower()
        _function+= ', accounts): \n\t'.expandtabs(4)
        _function+= f'{contract_name}.'+ query['name'] + '('
        for input in query['inputs']:
            _function+= f'{str(test_case[id])}, '
            id+=1
        _function+= '{"from": '+ f'accounts[{account}]' + '})\n\t'.expandtabs(4)
        _function += self.addFailAssertion()
        return _function, id
    
    # contractInstance.contractFunction(*inputs)
    def treatView(self, query, test_case, id):
        contract_name = self.contract_name.lower()
        _function= self.contract_name.lower()
        _function+= ', accounts): \n\t'.expandtabs(4)
        _function+= f'{contract_name}.'+ query['name'] + '('
        for input in query['inputs']:
            _function+= f'{str(test_case[id])}, '
            id+=1
        if (len(query['inputs']))>0:
            _function= _function[:-2]+ ')\n\t'.expandtabs(4)
        else:
            _function+= ')\n\t'.expandtabs(4)
        _function += self.addFailAssertion()
        return _function, id


