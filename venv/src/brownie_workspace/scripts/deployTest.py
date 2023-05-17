from brownie import accounts, network, Voting
import sys

sys.path.append("../")
import globalVars



def main():

    network.connect("development")
    accounts.add()
    account = accounts[0]
    print(globalVars.constructorInputs)
    contract_instance = Voting.deploy( * globalVars.constructorInputs ,  {'from' : account} )
    
    
    return contract_instance

