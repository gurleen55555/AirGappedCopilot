import os
import pickle

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical

SEQUENCE_LENGTH = 10

# Load dataset
df = pd.read_csv("data/network_data_lstm.csv")

features = df[["CPU", "Latency", "PacketLoss"]].values
labels = df["Status"].values

# Scale input features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Convert text labels into numbers
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

# Create sequences of the previous 10 readings
X = []
y = []

for i in range(SEQUENCE_LENGTH, len(df)):
    X.append(scaled_features[i - SEQUENCE_LENGTH:i])
    y.append(encoded_labels[i])

X = np.array(X)
y = to_categorical(np.array(y), num_classes=len(label_encoder.classes_))

# Split without shuffling because sequence order matters
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

# Build LSTM model
model = Sequential([
    LSTM(64, input_shape=(SEQUENCE_LENGTH, X.shape[2])),
    Dropout(0.2),
    Dense(32, activation="relu"),
    Dense(len(label_encoder.classes_), activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    epochs=50,
    batch_size=16,
    callbacks=[early_stopping],
    verbose=1
)

loss, accuracy = model.evaluate(X_test, y_test, verbose=0)

os.makedirs("models", exist_ok=True)

model.save("models/lstm_model.keras")

with open("models/scaler.pkl", "wb") as file:
    pickle.dump(scaler, file)

with open("models/label_encoder.pkl", "wb") as file:
    pickle.dump(label_encoder, file)

print(f"LSTM Model Trained Successfully! Test Accuracy: {accuracy:.2%}")