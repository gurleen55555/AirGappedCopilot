import numpy as np
import pandas as pd

np.random.seed(42)

rows = []
cpu = 35.0
latency = 70.0
packet_loss = 1.0

for timestamp in range(2000):
    # Gradual changes so consecutive readings are related
    cpu += np.random.normal(0, 3)
    latency += np.random.normal(0, 8)
    packet_loss += np.random.normal(0, 0.5)

    cpu = np.clip(cpu, 5, 100)
    latency = np.clip(latency, 10, 400)
    packet_loss = np.clip(packet_loss, 0, 15)

    # Occasionally simulate network degradation
    if np.random.random() < 0.04:
        cpu += np.random.uniform(15, 30)
        latency += np.random.uniform(40, 100)
        packet_loss += np.random.uniform(2, 5)

    # Occasionally simulate recovery
    if np.random.random() < 0.06:
        cpu -= np.random.uniform(10, 25)
        latency -= np.random.uniform(20, 70)
        packet_loss -= np.random.uniform(1, 4)

    cpu = np.clip(cpu, 5, 100)
    latency = np.clip(latency, 10, 400)
    packet_loss = np.clip(packet_loss, 0, 15)

    if cpu > 85 or latency > 250 or packet_loss > 8:
        status = "failure"
    elif cpu > 65 or latency > 150 or packet_loss > 4:
        status = "risk"
    else:
        status = "normal"

    rows.append([
        timestamp,
        round(cpu, 2),
        round(latency, 2),
        round(packet_loss, 2),
        status
    ])

df = pd.DataFrame(
    rows,
    columns=["Timestamp", "CPU", "Latency", "PacketLoss", "Status"]
)

df.to_csv("data/network_data_lstm.csv", index=False)

print("Generated 2000 sequential network readings.")
print(df["Status"].value_counts())