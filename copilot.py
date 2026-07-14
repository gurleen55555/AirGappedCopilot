from rag.embeddings import retrieve_runbook
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
issues = []

if cpu > 85:
    issues.append("High CPU Utilization")

if latency > 150:
    issues.append("High Network Latency")

if loss > 5:
    issues.append("Packet Loss")

if issues:
    query = ". ".join(issues)
else:
    query = "Normal Network State with safe CPU latency and packet loss"
rag_results = retrieve_runbook(query)

runbook = "\n\n".join(result["content"] for result in rag_results)
source = ", ".join(result["source"] for result in rag_results)

# Prompt for Phi-3
prompt = f"""
Network Metrics:

CPU={cpu}
Latency={latency}
Loss={loss}

Predicted Status={prediction}

Reference Runbook:
Use only the provided network metrics, prediction, and reference runbook.
Do not invent causes, actions, trends, or historical information.
If the runbook says the network is normal, do not report an anomaly.
If no relevant runbook is found, say "Not enough information."
{runbook}

Return answer in format:

Issue:
Cause:
Action:

Summarize the runbook in simple language.
Use exactly 3 short lines:
Issue:
Cause:
Action:
Maximum 30 words total.
Do not repeat the full runbook.
"""

response = ollama.chat(
    model="phi3",
    messages=[{"role": "user", "content": prompt}]
)

print("Prediction:", prediction)
print("Retrieved source:", source)
print()
print(response["message"]["content"])