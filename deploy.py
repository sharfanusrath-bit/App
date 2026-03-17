import json
from web3 import Web3

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
web3.eth.default_account = web3.eth.accounts[0]

# Load compiled contract
with open("compiled_code.json", "r") as file:
    compiled_sol = json.load(file)

abi = compiled_sol["contracts"]["TaskContract.sol"]["TaskContract"]["abi"]
bytecode = compiled_sol["contracts"]["TaskContract.sol"]["TaskContract"]["evm"]["bytecode"]["object"]

# Deploy contract
TaskContract = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = TaskContract.constructor().transact()
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt.contractAddress
print(f"Contract Deployed at: {contract_address}")

# Save contract address for later use
with open("contract_address.txt", "w") as file:
    file.write(contract_address)
