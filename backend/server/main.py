from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from blockchain_interface import contract, w3
import hashlib
from web3 import Web3

app = FastAPI()

# Global model
global_model = np.array([0.5, 0.5, 0.5])

current_round = 1
expected_clients = 3 
client_updates = {} 
submitted_clients = set()
trust_history = {}
client_address_mapping = {}

class ModelUpdate(BaseModel):
    client_id: str
    client_address: str
    weights: list

@app.get("/")
def root():
    return {"message": "Aggregator Server is running"}

@app.get("/get_global_model")
def get_global_model():
    return {
        "round": current_round,
        "weights": global_model.tolist()
    }


@app.post("/submit_update")
def submit_update(update: ModelUpdate):
    global client_updates, submitted_clients, current_round, global_model

    # 🔹 Prevent duplicate submission in same round
    if update.client_id in submitted_clients:
        return {"message": "Already submitted for this round"}

    client_addr = Web3.to_checksum_address(update.client_address)
    weights_array = np.array(update.weights)
    client_address_mapping[update.client_id] = client_addr

    # 🔥 1️⃣ Dynamic anomaly detection
    deviation = np.linalg.norm(weights_array - global_model)
    threshold_dynamic = 2.0 

    if deviation > threshold_dynamic:
        print("⚠ Malicious update detected!")

        tx = contract.functions.penalizeClient(client_addr).transact()
        w3.eth.wait_for_transaction_receipt(tx)

        new_trust = contract.functions.getTrust(client_addr).call()

        # Mark as submitted (so cannot spam)
        submitted_clients.add(update.client_id)

        return {
            "message": "Client penalized for malicious update",
            "new_trust": new_trust
        }

    # 🔥 2️⃣ Trust verification from blockchain
    trust = contract.functions.getTrust(client_addr).call()
    threshold_contract = contract.functions.THRESHOLD().call()

    if trust < threshold_contract:
        submitted_clients.add(update.client_id)

        return {
            "message": "Client rejected due to low trust",
            "trust": trust
        }

    # 🔥 Store valid update
    client_updates[update.client_id] = weights_array
    submitted_clients.add(update.client_id)

    return {
        "message": "Update accepted",
        "trust": trust,
        "current_round": current_round
    }

# 🔥 NEW: Aggregation endpoint
@app.post("/aggregate")
def aggregate():
    global global_model, current_round
    global client_updates, submitted_clients
    global trust_history, client_address_mapping

    if len(client_updates) == 0:
        return {"message": "No valid updates to aggregate"}

    # 🔥 1️⃣ Federated Averaging
    updates = list(client_updates.values())
    global_model = np.mean(updates, axis=0)

    # 🔥 2️⃣ Record trust for this round
    for client_id in submitted_clients:

        if client_id not in client_address_mapping:
            continue

        client_addr = client_address_mapping[client_id]
        trust = contract.functions.getTrust(client_addr).call()

        if client_id not in trust_history:
            trust_history[client_id] = []

        trust_history[client_id].append(trust)

    # 🔥 3️⃣ Prepare response
    response = {
        "message": "Aggregation complete",
        "new_global_model": global_model.tolist(),
        "next_round": current_round + 1,
        "trust_snapshot": trust_history
    }

    # 🔥 4️⃣ Clear round data
    client_updates.clear()
    submitted_clients.clear()

    # 🔥 5️⃣ Move to next round
    current_round += 1

    return response


@app.get("/trust_history")
def get_trust_history():
    return trust_history
   