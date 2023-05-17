# these are the variable that need to be interacted with between
#-> the scripts dir (brownie)
#-> the website dir (flask)

from brownie import accounts, network

network.connect('development')
accounts.add()
owner = accounts[0]


global contractName, constructorInputs, abi, bytecode, contractsInstancesMap
contractsInstancesMap = dict()