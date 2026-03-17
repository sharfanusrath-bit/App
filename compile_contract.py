from solcx import compile_standard, install_solc
import json

# Install Solidity compiler (if not already installed)
install_solc("0.8.0")

# Read Solidity contract
with open("TaskContract.sol", "r") as file:
    task_contract_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"TaskContract.sol": {"content": task_contract_file}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}},
    },
    solc_version="0.8.0",
)

# Save the compiled contract
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

print("Compilation successful!")