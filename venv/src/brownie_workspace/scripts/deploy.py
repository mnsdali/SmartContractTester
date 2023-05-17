
import brownie
from .setConfig import *
import sys

sys.path.append("../")



def main(contractName, contractOwner, constructorInputs ):

    contract = getattr(brownie, contractName)

    
   
    contract_instance = contract.deploy( 
                         *constructorInputs , {'from' : contractOwner})

    return contract_instance
    



