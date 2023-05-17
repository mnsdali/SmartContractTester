function handleSmartContractFunction( qID, btnID, btndiv){
               
    //alert(btnID)
  
    var myDiv = document.getElementById(qID);
    var inputs = myDiv.querySelectorAll("input");
    var resultInputs=[];

    // get the jinja2 abi to work in js
    var abi = '{{ abi | tojson }}';

    //transform it into a json var
    abi = JSON.parse(abi);

    var targetFunc;
    for( query of abi){
        if (query["name"]==btnID){
            targetFunc=query;
            break;
        }
    }
    
    for (i in targetFunc['inputs']){
        resultInputs.push(inputs[i].value);
       
    }
    
    var i = 0;
    var data = [targetFunc]; // falsk json ajax
    for (elem of resultInputs) {
        data.push( {['input'+i] : elem } );
    }

    

    $.ajax({
        type: "POST",
        url: "/process_sContract",
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: 'json',
        success: result => {
            var logElement = document.getElementById("log");
            if (result["type"] == "transaction"){
                
                if (result["status"]== "0") { //reverted
                    logElement.value += '\n~~~~~~~~~~~~~~~~~~~~  REVERTED ~~~~~~~~~~~~~~~~~~~~~\n';
                    logElement.value += "Transaction sent: "+ result["txid"]+"\n";
                    logElement.value += result["revert_type"]+": "+ result["revert_msg"]+ "...\n";
                    logElement.value +=  result["message"]+".......\n";
                    

                    let maxLines = 99; 
                    let lines = logElement.value.split('\n'); 
                    
                    if (lines.length > maxLines) { 
                        lines.splice(0, lines.length - maxLines); 
                        logElement.value = lines.join('\n'); 
                    }
                }
                else if(result["status"]== "1"){
                    
                  
                    function updateConsole(usdPrice){
                        let usd = parseFloat(usdPrice).toFixed(2);
                        let percentage =  ((parseInt(result["gas_used"])/ parseInt(result["gas_limit"]))*100).toFixed(2);
                        let logElement = document.querySelector('#log');
                        
                        logElement.value += '\n~~~~~~~~~~~~~~~~~~~~  SUCCESSFULLY MINED   ~~~~~~~~~~~~~~~~~~~~~~\n';
                        logElement.value += "Transaction hash: "+ result["tx_hash"]+"\n";
                        logElement.value += "Block: "+ result["block_number"]+"\t";
                        logElement.value += "Timestamp: "+ dateStamp+"\t";
                        logElement.value += "Value: "+ result["value"]+"\n";
                        logElement.value += "From: "+ result["sender"]+"\n";
                        logElement.value += "To: "+ result["receiver"]+"\n";
                        logElement.value += "Txn Feee: "+  txnFeeEth +" ETH " ;
                        logElement.value += "($"+(txnFeeEth*usd).toFixed(2)+")\n";
                        logElement.value += "Gas price: "+ result["gas_price"]+" gwei ("+eth+" ETH)\n";
                        
                        logElement.value += "Gas Limit & Usage by Txn: "+ result["gas_limit"]+" | "+ result["gas_used"];
                        logElement.value += " ("+ percentage+"%)\n";
                        
                        let maxLines = 45; 
                        let lines = logElement.value.split('\n'); 
                        
                        if (lines.length > maxLines) { 
                            lines.splice(0, lines.length - maxLines); 
                            logElement.value = lines.join('\n'); 
                        }
                        
                        
                        
                    }
                    const unixTimestamp = parseInt(result['timestamp']);
                    const dateObj = new Date(unixTimestamp * 1000);
                    const dateStamp = dateObj.toLocaleString();
                    const eth = parseFloat(result["gas_price"])/10**9;
                    
                    const txnFeeEth =  (eth*parseFloat(result["gas_used"]));                        
                    
                    getEthToUsdRatio().then(value  => {updateConsole(value);})
                    
                }
            }else{
                var logElement = document.getElementById("log");
                if (result["status"]== "0") { //reverted
                    logElement.value += '\n~~~~~~~~~~~~~~~~~~~~  REVERTED ~~~~~~~~~~~~~~~~~~~~~\n';
                    logElement.value += result["revert_type"]+": "+ result["revert_msg"]+ "...\n";
                    logElement.value +=  result["message"]+".......\n";
                    


                    let maxLines = 99; 
                    let lines = logElement.value.split('\n'); 
                    
                    if (lines.length > maxLines) { 
                        lines.splice(0, lines.length - maxLines); 
                        logElement.value = lines.join('\n'); 
                    }
                }

            }

            logElement.scrollTop = logElement.scrollHeight;
            const resultsDiv = document.createElement("div");
            resultsDiv.setAttribute('id', 'resp'+qID);
            resultsDiv.classList.add( 'my-2');
            const Container = document.getElementById(btndiv);
            const myChildElement = Container.querySelector("#"+"resp"+qID);
            if (myChildElement == null){
                Container.appendChild(resultsDiv);
                resultsDiv.innerHTML = "<h6>"+result["return_value"]+"</h6>";
            }else{
                myChildElement.innerHTML = "<h6>"+result["return_value"]+"</h6>";
            }
         
        } 
    });


    
   
    
}



async function getEthToUsdRatio() {
                
    const response = await fetch(`https://api.coinbase.com/v2/exchange-rates?currency=ETH`);
    const data = await response.json();
    const usdPrice = data.data.rates.USD;
    
    return usdPrice;
}

