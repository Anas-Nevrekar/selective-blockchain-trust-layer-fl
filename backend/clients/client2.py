from .client_base import FederatedClient
import numpy as np

# Create client using Ganache account[2]
client = FederatedClient(
    client_id="client_2",
    account_index=2
)

client.register()

# Get global model
global_weights, round_number = client.get_global_model()

# Train normally
local_weights = client.train(global_weights)

# 🔥 Controlled alternating attack:
# Attack only on EVEN rounds
if round_number % 2 == 0:
    print("⚠ client_2 sending malicious update this round")
    noise = np.random.normal(0, 5, size=len(local_weights))
    local_weights = local_weights + noise
else:
    print("✅ client_2 behaving honestly this round")

# Submit update
response = client.submit_update(local_weights, round_number)

print(response)