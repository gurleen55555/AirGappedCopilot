import pickle

import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

SEQUENCE_LENGTH = 10

# Load trained LSTM model
model = load_model("models/lstm_model.keras")

# Load scaler
with open("models/scaler.pkl", "rb") as file:
    scaler = pickle.load(file)

# Load label encoder
with open("models/label_encoder.pkl", "rb") as file:
    label_encoder = pickle.load(file)

# Load the latest network readings
df = pd.read_csv("data/network_data_lstm.csv")

latest_readings = df[["CPU", "Latency", "PacketLoss"]].tail(SEQUENCE_LENGTH)

# Apply the same scaling used during training
scaled_readings = scaler.transform(latest_readings.values)

# LSTM expects: batch, sequence length, features
input_sequence = np.expand_dims(scaled_readings, axis=0)

probabilities = model.predict(input_sequence, verbose=0)[0]
predicted_index = np.argmax(probabilities)
predicted_status = label_encoder.inverse_transform([predicted_index])[0]
confidence = probabilities[predicted_index]

print("Prediction:", predicted_status)
print(f"Confidence: {confidence:.2%}")