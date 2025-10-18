import os
import json
from weasyprint import HTML
from datetime import datetime
from web3 import Web3

# Connect to Sepolia testnet (replace with your Infura/Alchemy key or local node)
web3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/9862ef1feab24e0b9cb44e13d38f91d9'))
#https://sepolia.infura.io/v3/9862ef1feab24e0b9cb44e13d38f91d9
contract_address = "0x9A407C82FDdd646d4ca23DF1Cf25770793340d2C"  # Deployed DAO contract
contract_abi = [[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_member",
				"type": "address"
			}
		],
		"name": "addMember",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "outputId",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "approve",
				"type": "bool"
			}
		],
		"name": "voteOnOutput",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "approvedOutputs",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "outputId",
				"type": "uint256"
			}
		],
		"name": "isOutputApproved",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "members",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "votes",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]]  # Add ABI from compiled VisualDigestDAO.sol
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def compile_magazine():
    output_dir = "/app/output"
    html_content = "<html><body><h1>Visual Digest Weekly</h1>"
    
    # Collect approved agent outputs
    for file in os.listdir(output_dir):
        if file.endswith("_output.json"):
            output_id = hash(file) % 10000  # Simple ID for voting
            if contract.functions.isOutputApproved(output_id).call():
                with open(f"{output_dir}/{file}", "r") as f:
                    data = json.load(f)
                    html_content += f"<h2>{data['category']}</h2>"
                    html_content += f"<p>{data['summary']}</p>"
                    html_content += f"<img src='{data['visual']}' width='400'/>"
    
    html_content += "</body></html>"
    
    # Generate HTML and PDF
    timestamp = datetime.now().strftime("%Y%m%d")
    HTML(string=html_content).write_pdf(f"{output_dir}/magazine_{timestamp}.pdf")
    with open(f"{output_dir}/magazine_{timestamp}.html", "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    compile_magazine()
