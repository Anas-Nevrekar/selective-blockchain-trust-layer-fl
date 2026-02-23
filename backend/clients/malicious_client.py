from .client_base import FederatedClient
import numpy as np

client = FederatedClient(
    client_id="malicious_client",
    account_index=4
)

client.register()

global_weights, round_number = client.get_global_model()

# Strong poisoned update
malicious_weights = global_weights + np.array([50, 50, 50])

client.submit_update(malicious_weights, round_number)