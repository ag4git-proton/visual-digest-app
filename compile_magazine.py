import os
import json
from weasyprint import HTML
from datetime import datetime
from web3 import Web3

# Connect to Sepolia testnet (replace with your Infura/Alchemy key or local node)
web3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/YOUR_INFURA_KEY'))
contract_address = "0xYOUR_CONTRACT_ADDRESS"  # Deployed DAO contract
contract_abi = [...]  # Add ABI from compiled VisualDigestDAO.sol
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