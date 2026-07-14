import pickle
import ollama
from knowledge import get_runbook

# Model load
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

# Sample network metrics
cpu = 25
latency = 15
loss = 0

# Prediction
import pandas as pd

input_data = pd.DataFrame(
    [[cpu, latency, loss]],
    columns=["CPU", "Latency", "PacketLoss"]
)

prediction = model.predict(input_data)[0]
runbook = get_runbook(cpu, latency , loss)

# Prompt for Phi-3
prompt = f"""
Network Metrics:

CPU={cpu}
Latency={latency}
Loss={loss}

Predicted Status={prediction}

Reference Runbook:
Use only the provided network metrics, prediction, and runbook.
Do not mention historical trends, past weeks, seasonal load, or any information not given here.
If information is missing, say "Not enough information."
{runbook}

Return answer in format:

Issue:
Cause:
Action:

Maximum 40 words.
"""

response = ollama.chat(
    model="phi3",
    messages=[{"role": "user", "content": prompt}]
)

print("Prediction:", prediction)
print()
print(response["message"]["content"])