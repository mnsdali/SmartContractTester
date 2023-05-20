import os
import sys, json
import subprocess
from flask import Blueprint, render_template, request, session, flash, jsonify, redirect,send_file
from brownie import *
from brownie.exceptions import VirtualMachineError
from .test import compileSmartContract, brownieCompile, brownieTest
import re

sys.path.append('../random_test_generation')
from random_test_generation.Controller.testSmartContract import TestSmartContract


sys.path.append("../")
import globalVars


#define a blueprint
views = Blueprint('views', __name__)

# Modify the `autocompile` setting



#requirements to work with brownie project
brownie_path = "./brownie_workspace"
brownieName = "brownieWS"

proj = project.load(brownie_path, name=brownieName)

scripts_path = os.path.join(brownie_path, 'scripts')
##########
# {
#   "inputs": [
#     { "internalType": "bytes32", "name": "candidate", "type": "bytes32" }
#   ],
#   "name": "totalVotesFor",
#   "outputs": [{ "internalType": "uint8", "name": "", "type": "uint8" }],
#   "stateMutability": "view",
#   "type": "function"

# sCtype = [bytes32 , uint, String]
# }functProps

# [{'accountIndex': '0'}, {'input0': 'dali'}] sc_data  
#################
def fetchCallableInputs(functProps, sc_data):
    result = []
    inputIdx = 0
    print(sc_data)
    for query in sc_data:
        if (inputIdx == len(functProps['inputs'])): break;
        scType = functProps['inputs'][inputIdx]['type']
        for val in query.values():
            if '[]' in scType:
                val = val.split(',')
                if 'bytes' in scType:
                    val = list(map(lambda data : data.strip().encode('utf-8'),val))
                elif 'int' in scType:
                    val = list(map(lambda data : int(data), val))
                elif 'fixed' in scType:
                    val = list(map(lambda data : float(data), val)) 

                
            else:
                
                if 'bytes' in scType:
                    val = val.strip().encode('utf-8')
                elif 'int' in scType:
                    val = int(val)
                elif 'fixed' in scType:
                    val = float(val)
            result.append(val)

        inputIdx+=1
    return result

#################
def fetchConstructor(abi):
    constructorInputs = []
    for query in abi:
        if query["type"] == "constructor":
            for inp in query['inputs']:
                if '[]' in inp['type']:
                    arr = request.form.get(inp['name']).split(',')

                    if 'bytes' in inp['type']:
                        arr = list(map(lambda data : data.strip().encode('utf-8'),arr))
                    elif 'int' in inp['type']:
                        arr = list(map(lambda data : int(data), arr))
                    elif 'fixed' in inp['type']:
                        arr = list(map(lambda data : float(data), arr)) 

                    constructorInputs.append(arr)
                else:
                    elem = request.form.get(inp['name'])
                    if 'bytes' in inp['type']:
                        elem = elem.strip().encode('utf-8')
                    elif 'int' in inp['type']:
                        elem = int(elem)
                    elif 'fixed' in inp['type']:
                        elem = float(elem)
                    constructorInputs.append(elem)
    return constructorInputs

def fineTuneOutput(out , functProps):
    n = len(functProps)
    if n == 1:
        if '[]' in functProps[0]['type']:
            if 'bytes' in functProps[0]['type']:
                out=list(map(lambda s : s.decode().strip('\x00'), out))
        else:
            if 'bytes' in functProps[0]['type']:
                out = out.decode().rstrip('\x00')
    else :
        for i in range(n):
            if '[]' in functProps[i]['type']:
                if 'bytes' in functProps[i]['type']:
                    out[i]=list(map(lambda s : s.decode().strip('\x00'), out[i]))
            else:
                if 'bytes' in functProps[i]['type']:
                    out[i] = out[i].decode().strip('\x00')
    return out

def fineTuneOutputPhase2(out, outVals):
    for i in range(len(out)):
        out[i] = outVals
    return out
#################
def createTestTemplate(contract_name, contract_instance, contract_abi):

    test_template= "import pytest"
    for query in contract_abi:
        if query['type']=='function':
            func ="\n\ndef test_"+ query['name'] + "(): \n\tpass".expandtabs(4)
            test_template+=func
    
    return test_template

#decorator
@views.route('/')
def home():
    return render_template("base.html")



@views.route('/compiled', methods=["GET","POST"])
def compilationPhase():
    global proj
    if request.method == 'POST':
        contract_name = request.form.get('fileName')
        
        if contract_name == '':
            flash('You need to choose a smart contract before procceeding!', category="error")
            return render_template("base.html")
        
        
        if 'compileBtn' in request.form:
            file= request.files['file']
            
            
            file.save(os.path.join(brownie_path+"/contracts", contract_name))
            
            compiledContractName = compileSmartContract(contract_name)
            brownieCompile(contract_name)
            session['contractName'] = compiledContractName
            session['contractFileName'] = contract_name

            # reload the project 
            proj.close()
            proj = project.load(brownie_path, name=brownieName)
            #print(compiledContractName)
            # fetch the abi
            abi = json.dumps(proj._build.get(compiledContractName)['abi'])
            loaded_abi= json.loads(abi)

            session['abi'] = loaded_abi
            
            flash("the smart contract has been compiled successfully and is ready for deployment!", category="success")
            return render_template("compile.html", session=session, abi = loaded_abi)  
    else:
        return render_template("base.html")
    

@views.route('/deployed', methods=['POST', 'GET'])
def deploymentPhase():
    global proj
    if request.method == 'POST':
        if 'deployBtn' in request.form:
            
            if not session.get('contractName'):
                flash("you need to compile the smart contract before deployment", category="error")
                return render_template("base.html")
            else:
                
                contractName = session.get("contractName")
                
                abi = json.dumps(proj._build.get(contractName)['abi'])
                loaded_abi= json.loads(abi)
                
                
                constructorInputs = fetchConstructor(loaded_abi)
                session['constructor_inputs'] = constructorInputs
                globalVars.contractsInstancesMap[contractName] = run('deploy.py', args=(contractName, globalVars.owner, constructorInputs))

                accs = [(globalVars.accounts[i].address, (globalVars.accounts[i].balance() *1e-18)) for i in range(10)]
                session['accs'] = accs
                flash("the smart contract has been deployed successfully", category="success" )        
                return render_template("deployed.html", abi=loaded_abi, accs=accs)
        
        elif 'backBtn' in request.form:
            return  render_template("base.html")
    else:
        return render_template("base.html")


@views.route('/process_sContract', methods=['POST', 'GET'])
def process_sContract():
    if request.method == "POST":
        contractName = session.get("contractName")
        sc_data = request.get_json()
        results = {}
        tx = None
        #here we will get the function from deployed smart contract instance
        # sContractInstance.func(inp)
        print(sc_data)
        callFunction = getattr(
            globalVars.contractsInstancesMap[contractName], sc_data[0]["name"])

        if len(sc_data[0]["inputs"]) == 0:  #this is a function that doesn't contain any input
            
            try:
                if sc_data[0]["stateMutability"] in ["view","pure" ]: 
                    #calling the function
                    out = callFunction()
                    

                elif sc_data[0]["stateMutability"] == "nonpayable" :
                    
                    tx = callFunction( {'from' : globalVars.accounts[int(sc_data[1]['accountIndex'])]} )
                    out = tx.return_value
                    
                    results = {
                        "type": "transaction",
                        "tx_hash" : tx.txid,
                        "nonce" : tx.nonce,
                        "block_number" : tx.block_number,
                        "gas_limit" : tx.gas_limit,
                        "gas_price" : tx.gas_price,
                        "gas_used" : tx.gas_used,
                        "receiver" : tx.receiver,
                        "sender" : tx.sender.address,
                        "status" : tx.status,
                        "timestamp" : tx.timestamp,
                        "value": tx.value,
                        "contractBalance": globalVars.contractsInstancesMap[contractName].balance()/1e18
                    }
                    
                    
                elif sc_data[0]["stateMutability"] == "payable" :
                    tx = callFunction( { 'from' : globalVars.accounts[int(sc_data[1]['accountIndex'])], 
                                         'amount' :  float(sc_data[2]['amount']) } )
                    out = tx.return_value
                    
                    results = {
                        "type": "transaction",
                        "tx_hash" : tx.txid,
                        "nonce" : tx.nonce,
                        "block_number" : tx.block_number,
                        "gas_limit" : tx.gas_limit,
                        "gas_price" : tx.gas_price,
                        "gas_used" : tx.gas_used,
                        "receiver" : tx.receiver,
                        "sender" : tx.sender.address,
                        "status" : tx.status,
                        "timestamp" : tx.timestamp,
                        "value": tx.value,
                        "contractBalance": globalVars.contractsInstancesMap[contractName].balance()/1e18
                    }
               
            except VirtualMachineError as e:
                results["status"] = 0
                results["message"] = e.message
                results["revert_msg"] = e.revert_msg
                results["revert_type"] = e.revert_type
                results["txid"] = e.txid
                
                
                return jsonify(results)  
            
        else: #this function contains inputs
            
            try:
                if sc_data[0]["stateMutability"] in ["view","pure" ]: 
                    itms = fetchCallableInputs(sc_data[0],sc_data[2:])
                    #print(itms)
                    results = {"type": "call"}
                    out = callFunction(*itms) 
                    

                elif sc_data[0]["stateMutability"] == "nonpayable" :
                    itms = fetchCallableInputs(sc_data[0],sc_data[2:])
                    #print(itms)
                    print(globalVars.accounts[int(sc_data[1]['accountIndex'])], " xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                    tx= callFunction(*itms, 
                                     { 'from' : globalVars.accounts[ int(sc_data[1]['accountIndex']) ]
                                      
                                      }
                                     )
                                         
                    

                    out = tx.return_value
                    results = {
                                    "type": "transaction",
                                    "tx_hash" : tx.txid,
                                    "nonce" : tx.nonce,
                                    "block_number" : tx.block_number,
                                    "gas_limit" : tx.gas_limit,
                                    "gas_price" : tx.gas_price,
                                    "gas_used" : tx.gas_used,
                                    "receiver" : tx.receiver,
                                    "sender" : tx.sender.address,
                                    "status" : tx.status,
                                    "timestamp" : tx.timestamp,
                                    "value": tx.value,
                                    "contractBalance": globalVars.contractsInstancesMap[contractName].balance()/1e18
                    }
                elif sc_data[0]["stateMutability"] == "payable" :
                    itms = fetchCallableInputs(sc_data[0],sc_data[3:])
                    tx = callFunction(*itms, { 'from' : globalVars.accounts[int(sc_data[1]['accountIndex'])], 
                                         'amount' :  float(sc_data[2]['amount']) } )
                    out = tx.return_value
                    results = {
                                    "type": "transaction",
                                    "tx_hash" : tx.txid,
                                    "nonce" : tx.nonce,
                                    "block_number" : tx.block_number,
                                    "gas_limit" : tx.gas_limit,
                                    "gas_price" : tx.gas_price,
                                    "gas_used" : tx.gas_used,
                                    "receiver" : tx.receiver,
                                    "sender" : tx.sender.address,
                                    "status" : tx.status,
                                    "timestamp" : tx.timestamp,
                                    "value": tx.value,
                                    "contractBalance": globalVars.contractsInstancesMap[contractName].balance()/1e18
                    }

            except VirtualMachineError as e:
                if sc_data[0]["stateMutability"] == "nonpayable" :
                    results = {"type": "transaction"}
                results["status"] = 0
                results["message"] = e.message
                results["revert_msg"] = e.revert_msg
                results["revert_type"] = e.revert_type
                results["txid"] = e.txid
                print("error is " , e.revert_msg)
                return jsonify(results)
                
        
        outVals = out 
        if tx != None and out != None:
            
            outVals = fineTuneOutput(outVals , sc_data[0]['outputs'])
            out = fineTuneOutputPhase2(out, outVals)
            results['return_value'] = str(out)
            
            
        else:
            outVals = fineTuneOutput(outVals , sc_data[0]['outputs'])
            results['return_value'] = str(outVals)
            print(results['return_value'])

        return jsonify(results)





@views.route('/process_testGeneration', methods=['POST', 'GET'])
def processTestGenerationPhase():
    global proj
    if request.method == 'POST':        
        if not session.get('contractName'):
            flash("you need to compile the smart contract before deployment", category="error")
            return render_template("base.html")
        

        contract_name = session.get('contractName')
        contract_instance = globalVars.contractsInstancesMap[contract_name]
        contract_abi = proj._build.get(contract_name)['abi']
        wallet = globalVars.accounts
        constructorInputs = session['constructor_inputs']

        test_smart_contract = TestSmartContract(contract_abi, wallet, contract_name, contract_instance, constructorInputs)
        test_template, test_case = test_smart_contract.generateTestFileTemplate()

        print(test_case)
        test_cases_file_path = f'./test_cases/test_cases{contract_name}.json'
        test_template_file_path  = f'./brownie_workspace/tests/test_{contract_name}.py'
        if os.path.isfile(test_cases_file_path):
            with open(test_cases_file_path, 'r') as jsonFile:
                json_test_case = json.load(jsonFile)
                json_test_case.append(test_case)
        else:
            json_test_case = [test_case]
        
        with open(test_cases_file_path, 'w') as jsonFile:
            json.dump(json_test_case, jsonFile, indent=4)

        with open(test_template_file_path, 'w') as brownie_testFile:
            brownie_testFile.write(test_template)


        return jsonify({'test_template': test_template})

        




@views.route('/processFunctions')
def processFuncs():
    return render_template("functions.html", abi = session["abi"], accs = session['accs'])



@views.route('/download_test_cases')
def download_test_cases():
    contract_name = session.get('contractName')
    filename = f'../test_cases/test_cases{contract_name}.json'
    return send_file(filename, as_attachment=True)

@views.route('/download_brownie_test_python_code')
def download_brownie_test_python_code():
    contract_name = session.get('contractName')
    filename = f'../brownie_workspace/tests/test_{contract_name}.py'
    return send_file(filename, as_attachment=True)
       

@views.route('/testCoverage')
def coverage_report():
    contract_name = session.get('contractName')
    filename = f'../website/templates/reports/coverage_report_{contract_name}.html'
    return send_file(filename)

@views.route('/loading')
def loadingScreen():
    filename = f'../website/templates/loading.html'
    return send_file(filename)

      



# coverage part
def perpare_coverage_props():
    contract_name = session.get('contractName')
    contract_file_name = session.get('contractFileName')
    contract_file_path = f'./brownie_workspace/contracts/{contract_file_name}'
    with open(contract_file_path, 'r') as contract:
        contractCode = contract.read()
    
    with open('./brownie_workspace/reports/coverage.json', 'r') as report:
        coverage = json.load(report)
    
    contract_highlights_branches = coverage['highlights']['branches'][contract_name]
    contract_highlights_statements = coverage['highlights']['statements'][contract_name]

    statementsText = []
    numberOfNewLines= 0  
    lastIndex = 0
    for k, v in contract_highlights_statements.items():
        if v != []:
            v = sorted(v,  key=lambda x: x[0])
            for x in v:
                portion = contractCode[lastIndex:x[0]]
                if portion != "":
                    numberOfNewLines+= portion.count('\n')
                    statementsText.append((portion , 'normal'))
                    lastIndex = x[1]
                
                realPortion = contractCode[x[0]:x[1]]
                print(realPortion)
                statementsText.append((realPortion  , x[2]))
    statementsText.append((contractCode[lastIndex:] ,'normal'))
    
    branchesText = []
    numberOfNewLines= 0  
    lastIndex = 0
    for k, v in contract_highlights_branches.items():
        if v != []:
            v = sorted(v,  key=lambda x: x[0])
            for x in v:
                portion = contractCode[lastIndex:x[0]]
                if portion != "":
                    numberOfNewLines+= portion.count('\n')
                    branchesText.append((portion , 'normal'))
                    lastIndex = x[1]
                
                realPortion = contractCode[x[0]:x[1]]
                print(realPortion)
                branchesText.append((realPortion  , x[2]))
    branchesText.append((contractCode[lastIndex:] ,'normal'   ))      

    return statementsText, branchesText, contractCode.count('\n')


@views.route('/process_testCoverage', methods=['POST', 'GET'])
def processTestCoveragePhase():
    global proj
    if request.method == 'POST':        
        if not session.get('contractName'):
            flash("you need to compile the smart contract before deployment", category="error")
            return render_template("base.html")
        
        
        contract_name = session.get('contractName')

        sc_data = request.get_json()
        with open(f'./brownie_workspace/tests/test_{contract_name}.py', 'w') as test_template_file:
            test_template_file.write(sc_data['test_template'])

        brownieTest(contract_name)
        statementsText, branchesText, nbLines = perpare_coverage_props()
        html = generate_html(statementsText, branchesText, nbLines)

        with open(f'./website/templates/reports/coverage_report_{contract_name}.html', 'w') as coverageFile:
            coverageFile.write(html)
            
        return jsonify({'success': 'w' })


def generate_html(statementsText, branchesText, nbLines ):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    </head>

    <body>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro:ital,wght@1,500&display=swap');
    .red, .yellow, .orange, .normal, .green{
    font-family: 'Source Code Pro', monospace;
    font-size: 13px;
    color :rgb(18, 24, 27);

    }

    .red{
        background: #ff0000;
    }

    .yellow{
        background: #ffd500;
    }

    .orange{
        background: #ff8c00;
    }

    .green{
        background: #029902;
    }

    .normal{
        background: #ffffff;
    }
    </style>
    <div id="coverageReport" style="display:flex" class="normal">
    <div id="nbLines" style="width:8%">
    """
    
    for i in range(1,nbLines+2):
        html += f'{i}<br>'
    
    html +="""
    </div>
    <div id="code" style="width:92%">
    <div id="statementsHighlights">
    """
    
    txt1 = ''
    for k, v in statementsText:
        if v == 'green':
            txt1 += '<span class="green" >'+k+'</span>';
        
        elif v == 'red':
            txt1 += '<span class="red" >'+k+'</span>';
        
        elif v == 'yellow':
            txt1 += '<span class="yellow" >'+k+'</span>';
        
        elif v == 'orange':
            txt1 += '<span class="orange" >'+k+'</span>';
        
        else:
            txt1 += '<span class="normal" >'+k+'</span>';
    
    txt1 = txt1.replace('\n', '<br>')
    html += txt1
    html += '</div>'
    html += '<div id="branchesHighlights" style="display:none">'

    txt1 = ''
    for k, v in branchesText:
        if v == 'green':
            txt1 += '<span class="green" >'+k+'</span>';
        
        elif v == 'red':
            txt1 += '<span class="red" >'+k+'</span>';
        
        elif v == 'yellow':
            txt1 += '<span class="yellow" >'+k+'</span>';
        
        elif v == 'orange':
            txt1 += '<span class="orange" >'+k+'</span>';
        
        else:
            txt1 += '<span class="normal" >'+k+'</span>';

    txt1 = txt1.replace('\n', '<br>')
    html += txt1
    html += '</div></div></body></html>'

    return html



    

