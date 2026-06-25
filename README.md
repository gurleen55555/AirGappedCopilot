# 🚀 AstraGrid AI

### Air-Gapped Predictive Copilot for Secure MPLS Operations

AstraGrid AI is an offline AI-powered network operations assistant designed for secure and mission-critical environments. The system analyzes network telemetry, detects anomalies, predicts failures using Machine Learning, and provides root-cause analysis with corrective actions through a locally hosted Phi-3 model.

> No Internet Required • Fully Air-Gapped • Local AI Inference • Real-Time Monitoring

---

## 📌 Problem Statement

Modern secure networks generate massive volumes of telemetry and logs. Operators often struggle to identify anomalies, predict failures, and determine corrective actions in real time.

AstraGrid AI addresses this challenge by combining:

* Machine Learning-based failure prediction
* Local LLM-powered analysis
* Network telemetry monitoring
* Incident reporting
* Air-gapped deployment

---

## ✨ Features

* 🔒 Fully Air-Gapped Operation
* 🤖 Local AI Assistant (Phi-3 via Ollama)
* 📊 Real-Time Network Telemetry Dashboard
* ⚠️ Anomaly Detection
* 📈 Failure Prediction using Random Forest
* 📁 Network Log Upload & Analysis
* 📝 Incident Report Generation
* 📚 Incident History Tracking
* 🎯 Risk Assessment Engine
* 🌐 No Cloud Dependency

---

## 🏗️ System Architecture

```text
Network Logs / Telemetry
          │
          ▼
   Feature Extraction
          │
          ▼
    Anomaly Detection
          │
          ▼
  ML Prediction Engine
          │
          ▼
     Risk Assessment
          │
          ▼
     Phi-3 Copilot
          │
          ▼
 Root Cause Analysis
          │
          ▼
 Corrective Actions
          │
          ▼
 Incident Report
```

## 🛠️ Technology Stack

### Frontend

* Streamlit

### Machine Learning

* Scikit-Learn
* Random Forest Classifier
* Pandas
* NumPy

### AI Layer

* Ollama
* Phi-3 Mini

### Backend

* Python

---

## 📂 Project Structure

```text
AirGappedCopilot/
│
├── app.py
├── copilot.py
├── knowledge.py
│
├── data/
│   ├── network_data.csv
│   └── incidents.csv
│
├── ml/
│   ├── generate_dataset.py
│   └── train_model.py
│
├── models/
│   └── model.pkl
│
├── tests/
│   └── phi_test.py
│
└── venv/
```

---

## ⚙️ Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Environment

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install pandas numpy scikit-learn streamlit joblib
```

### 4. Install Ollama

Pull the Phi-3 model:

```bash
ollama pull phi3
```

Verify installation:

```bash
ollama list
```

---

## 📊 Dataset Generation

Generate a synthetic dataset of 500 network telemetry records:

```bash
python ml/generate_dataset.py
```

---

## 🧠 Model Training

Train the prediction model:

```bash
python ml/train_model.py
```

This creates:

```text
models/model.pkl
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application will start at:

```text
http://localhost:8501
```

---

## 🧪 Sample Test Cases

### Normal Network

| Metric      | Value |
| ----------- | ----- |
| CPU         | 35%   |
| Latency     | 60 ms |
| Packet Loss | 0%    |

Prediction:

```text
NORMAL
```

### Risk Condition

| Metric      | Value  |
| ----------- | ------ |
| CPU         | 75%    |
| Latency     | 170 ms |
| Packet Loss | 4%     |

Prediction:

```text
RISK
```

### Failure Condition

| Metric      | Value  |
| ----------- | ------ |
| CPU         | 95%    |
| Latency     | 300 ms |
| Packet Loss | 12%    |

Prediction:

```text
FAILURE
```

---

## 🎯 Use Cases

* MPLS Operations Monitoring
* Secure Enterprise Networks
* Defense Communication Systems
* Telecom Infrastructure Monitoring
* Air-Gapped Network Environments
* Network Operations Centers (NOC)

---

## 🔮 Future Scope

* SNMP Integration
* Real-Time Device Monitoring
* Topology Visualization
* Predictive Maintenance
* Multi-Node Telemetry Collection
* Threat Intelligence Integration

---

## 👥 Team

### Team Bhaskar

---

## 📄 License

This project is developed for hackathon and educational purposes.
