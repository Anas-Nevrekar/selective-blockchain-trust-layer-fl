from web3 import Web3
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

print("Blockchain connected:", w3.is_connected())

# Set default account (server acts as aggregator authority)
w3.eth.default_account = w3.eth.accounts[0]

# 🔹 Replace with your deployed contract address
contract_address = Web3.to_checksum_address("0x31aa312dA17359581818b332B0e5e25211834c73")

# 🔹 Paste your ABI here (copy from trustLayer.json)
abi = [
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "client",
          "type": "address"
        }
      ],
      "name": "Blacklisted",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "client",
          "type": "address"
        }
      ],
      "name": "ClientRegistered",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "client",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "round",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "bytes32",
          "name": "hash",
          "type": "bytes32"
        }
      ],
      "name": "HashSubmitted",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "address",
          "name": "client",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "newTrust",
          "type": "uint256"
        }
      ],
      "name": "TrustUpdated",
      "type": "event"
    },
    {
      "inputs": [],
      "name": "INITIAL_TRUST",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "PENALTY",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "THRESHOLD",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
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
      "name": "blacklisted",
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
          "name": "client",
          "type": "address"
        }
      ],
      "name": "getTrust",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "client",
          "type": "address"
        }
      ],
      "name": "penalizeClient",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "registerClient",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "round",
          "type": "uint256"
        },
        {
          "internalType": "bytes32",
          "name": "hash",
          "type": "bytes32"
        }
      ],
      "name": "submitHash",
      "outputs": [],
      "stateMutability": "nonpayable",
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
      "name": "trustScore",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
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
      "name": "updateHashes",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
] 

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)