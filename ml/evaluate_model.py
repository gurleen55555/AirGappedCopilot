import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)
from tensorflow.keras.models import load_model

SEQUENCE_LENGTH = 10

# Load dataset
df = pd.read_csv("data/network_data_lstm.csv")

features = df[["CPU", "Latency", "PacketLoss"]].values
labels = df["Status"].values

# Load preprocessing objects
with open("models/scaler.pkl", "rb") as file:
    scaler = pickle.load(file)

with open("models/label_encoder.pkl", "rb") as file:
    label_encoder = pickle.load(file)

# Load trained LSTM model
model = load_model("models/lstm_model.keras")

# Apply the same scaling used during training
scaled_features = scaler.transform(features)

# Recreate sequences
X = []
y = []

for i in range(SEQUENCE_LENGTH, len(df)):
    X.append(scaled_features[i - SEQUENCE_LENGTH:i])
    y.append(labels[i])

X = np.array(X)
y = np.array(y)

# Use the same final 20% as test data
split_index = int(len(X) * 0.8)

X_test = X[split_index:]
y_test = y[split_index:]

# Predict probabilities and classes
probabilities = model.predict(X_test, verbose=0)
predicted_indices = np.argmax(probabilities, axis=1)
y_pred = label_encoder.inverse_transform(predicted_indices)

# Print evaluation results
accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0,
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0,
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0,
)

print(f"Accuracy: {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"F1-Score: {f1:.2%}")
print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        labels=label_encoder.classes_,
        zero_division=0,
    )
)

# Create confusion matrix
matrix = confusion_matrix(
    y_test,
    y_pred,
    labels=label_encoder.classes_,
)

display = ConfusionMatrixDisplay(
    confusion_matrix=matrix,
    display_labels=label_encoder.classes_,
)

display.plot(values_format="d")
plt.title("LSTM Confusion Matrix")
plt.tight_layout()
plt.savefig("models/lstm_confusion_matrix.png", dpi=200)
plt.show()

print("Confusion matrix saved to models/lstm_confusion_matrix.png")