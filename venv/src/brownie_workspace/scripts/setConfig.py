from web3 import Web3

class DeploymentConfig:
    

    def __init__(self, abi, bytecode, contractName, deploymentAccount, network, chainID):
        self.abi = abi
        self.bytecode = bytecode
        self.contractName = contractName
        self.deploymentAccount = deploymentAccount
        self.address = deploymentAccount.address
        self.private_key = deploymentAccount.private_key
        self.w3 = Web3(Web3.HTTPProvider(network))
        self.chain_id = chainID
        self.ContactList = self.w3.eth.contract(abi=abi, bytecode=bytecode) #contract
   

    def getContract(self):
        return self.ContractList


    ## Get the number of latest transaction
    def getNonce(self):
        return self.w3.eth.getTransactionCount(self.address)
    
    def buildTransaction(self, constructorArgs ):
        transaction = self.ContactList.constructor().buildTransaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "from": self.address,
                "nonce": self.getNonce(),
            }
        )
        return transaction
    
    def signTransaction(self, transaction):
        sign_transaction = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        print("Deploying Contract!")
        return sign_transaction
    
    def sendTransaction(self, sign_transaction):
        transaction_hash = self.w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
        return transaction_hash
        
    
    def deploy(self, constructorArgs ):
        transaction = self.buildTransaction(constructorArgs)
        sign_transaction = self.signTransaction(transaction=transaction)
        transaction_hash = self.sendTransaction(sign_transaction=sign_transaction)
       
        print("Waiting for transaction to finish...")
        transaction_receipt = self.w3.eth.wait_for_transaction_receipt(transaction_hash)
        print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")

        sContract = self.w3.eth.contract(address=transaction_receipt.contractAddress, abi=self.abi)
        return sContract
    
