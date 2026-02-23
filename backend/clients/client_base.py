import requests
import numpy as np
import hashlib
from web3 import Web3
abi = [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
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
SERVER_URL = "http://127.0.0.1:8000"
GANACHE_URL = "http://127.0.0.1:7545"
CONTRACT_ADDRESS = "0x31aa312dA17359581818b332B0e5e25211834c73"

class FederatedClient:

    def __init__(self, client_id, account_index):
        self.client_id = client_id

        # Blockchain setup
        self.w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
        self.account = self.w3.eth.accounts[account_index]
        self.w3.eth.default_account = self.account

        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(CONTRACT_ADDRESS),
            abi=abi
        )

    def register(self):
        try:
            self.contract.functions.registerClient().transact()
            print(f"{self.client_id} registered on blockchain")
        except:
            print(f"{self.client_id} already registered")

    def get_global_model(self):
        response = requests.get(f"{SERVER_URL}/get_global_model")
        data = response.json()
        return np.array(data["weights"]), data["round"]

    def train(self, global_weights):
        return global_weights + np.random.normal(0, 0.1, size=global_weights.shape)

    def submit_update(self, weights, round_number):
        # Hash weights
        weights_bytes = weights.tobytes()
        hash_hex = hashlib.sha256(weights_bytes).hexdigest()
        hash_bytes32 = Web3.to_bytes(hexstr=hash_hex)

        # Submit hash to blockchain
        try:
            self.contract.functions.submitHash(round_number, hash_bytes32).transact()
        except Exception as e:
            print("Blockchain rejected transaction:", e)
            return

        # Send weights to server
        payload = {
            "client_id": self.client_id,
            "client_address": self.account,
            "weights": weights.tolist()
        }

        response = requests.post(f"{SERVER_URL}/submit_update", json=payload)
        print(response.json())