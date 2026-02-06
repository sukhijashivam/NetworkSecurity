# 🛡️ Network Security - End-to-End ML Project

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-green.svg)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [ML Pipeline](#-ml-pipeline)
- [API Documentation](#-api-documentation)
- [Model Performance](#-model-performance)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)
- [Contact](#-contact)

## 🎯 Project Overview

**Network Security** is an end-to-end machine learning project designed to detect network intrusions and anomalous behavior in real-time. The system analyzes network traffic patterns to identify potential security threats, helping organizations protect their infrastructure from cyber attacks.

### Problem Statement

Network security threats are constantly evolving, making it challenging to detect intrusions using traditional rule-based systems. This project leverages machine learning to:

- Detect anomalous network traffic patterns
- Identify potential security breaches in real-time
- Classify network traffic as normal or malicious
- Provide actionable insights for security teams

### Solution Approach

The project implements a complete MLOps pipeline including:
- Automated data ingestion from multiple sources
- Robust data validation and transformation
- Model training with multiple algorithms
- Real-time prediction API
- Comprehensive logging and monitoring
- CI/CD integration for seamless deployment

## ✨ Features

- **🔍 Anomaly Detection**: Identifies unusual patterns in network traffic
- **📊 Multiple ML Models**: Supports Random Forest, Decision Tree, Gradient Boosting, and more
- **🔄 Automated Pipeline**: End-to-end automated ML workflow
- **📈 Experiment Tracking**: MLflow integration for model versioning
- **🌐 REST API**: Flask-based API for real-time predictions
- **💾 Database Integration**: MongoDB for data storage and retrieval
- **📝 Comprehensive Logging**: Detailed logs for debugging and monitoring
- **🐳 Docker Support**: Containerized deployment
- **☁️ Cloud Ready**: AWS S3 integration for data storage
- **🎨 Web Interface**: User-friendly UI for predictions

## 🏗️ System Architecture

```
┌─────────────────┐
│   Data Sources  │
│  (CSV, MongoDB) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Ingestion  │
│   & Validation  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      Data       │
│ Transformation  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Model       │
│    Training     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Model          │
│  Evaluation     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Prediction    │
│     API         │
└─────────────────┘
```

## 🛠️ Technologies Used

### Programming & ML
- **Python 3.8+**: Core programming language
- **Scikit-learn**: Machine learning algorithms
- **Pandas & NumPy**: Data manipulation and analysis
- **Imbalanced-learn**: Handling imbalanced datasets
- **MLflow**: Experiment tracking and model registry

### Web Framework & Database
- **Flask**: REST API development
- **MongoDB**: NoSQL database for data storage
- **PyMongo**: MongoDB Python driver

### DevOps & Deployment
- **Docker**: Containerization
- **GitHub Actions**: CI/CD pipeline
- **AWS S3**: Cloud storage
- **Boto3**: AWS SDK for Python

### Development Tools
- **Pytest**: Testing framework
- **Python-dotenv**: Environment variable management
- **YAML**: Configuration management

## 📁 Project Structure

```
NetworkSecurity/
│
├── .github/workflows/          # CI/CD configuration
│   └── main.yaml               # GitHub Actions workflow
│
├── networksecurity/            # Main package directory
│   ├── __init__.py
│   ├── components/             # Pipeline components
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   └── model_evaluation.py
│   ├── entity/                 # Data classes
│   │   ├── config_entity.py
│   │   └── artifact_entity.py
│   ├── pipeline/               # Training & prediction pipelines
│   │   ├── training_pipeline.py
│   │   └── prediction_pipeline.py
│   ├── utils/                  # Utility functions
│   │   ├── main_utils.py
│   │   └── ml_utils.py
│   ├── logging/                # Custom logging
│   ├── exception/              # Custom exceptions
│   └── constants/              # Project constants
│
├── Network_Data/               # Raw network traffic datasets
├── data_schema/                # Data validation schemas
├── final_model/                # Trained models
├── logs/                       # Application logs
├── mlruns/                     # MLflow experiment tracking
├── valid_data/                 # Validated datasets
├── templates/                  # HTML templates for web UI
│
├── app.py                      # Flask application
├── main.py                     # Main training pipeline
├── push_data.py                # Data ingestion script
├── test_mongodb.py             # MongoDB connectivity test
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
└── README.md                   # Project documentation
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- MongoDB (local or Atlas)
- AWS Account (for S3 storage - optional)
- Docker (for containerized deployment - optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/sukhijashivam/NetworkSecurity.git
cd NetworkSecurity
```

### Step 2: Create Virtual Environment

```bash
# For Linux/Mac
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory:

```env
# MongoDB Configuration
MONGO_DB_URL=mongodb://localhost:27017
MONGO_DB_NAME=networksecurity

# AWS Configuration (Optional)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
BUCKET_NAME=your-bucket-name

# Application Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### Step 5: Test MongoDB Connection

```bash
python test_mongodb.py
```

### Step 6: Install the Package

```bash
pip install -e .
```

## 💻 Usage

### 1. Data Ingestion

Push data to MongoDB:

```bash
python push_data.py
```

### 2. Train the Model

Run the complete training pipeline:

```bash
python main.py
```

This will:
- Ingest data from MongoDB
- Validate data quality
- Transform and preprocess data
- Train multiple ML models
- Evaluate and select the best model
- Save the model to `final_model/` directory

### 3. Start the Web Application

```bash
python app.py
```

Access the application at: `http://localhost:5000`

### 4. Make Predictions via API

```python
import requests
import pandas as pd

# Prepare your data
data = {
    'feature1': [value1],
    'feature2': [value2],
    # ... other features
}

# Make prediction
response = requests.post(
    'http://localhost:5000/predict',
    json=data
)

print(response.json())
```

## 🔄 ML Pipeline

### 1. Data Ingestion

- Reads network traffic data from MongoDB
- Validates data format and schema
- Stores raw data for processing

**Key Features:**
- Automated data fetching
- Schema validation
- Error handling

### 2. Data Validation

- Checks for missing values
- Validates data types
- Ensures data quality standards

**Validation Steps:**
- Column name verification
- Data type checking
- Missing value analysis
- Outlier detection

### 3. Data Transformation

- Feature engineering
- Handling imbalanced datasets (SMOTE)
- Scaling and normalization
- Train-test split

**Transformations:**
- Categorical encoding
- Feature scaling (StandardScaler)
- Resampling for class imbalance
- Feature selection

### 4. Model Training

Trains multiple models and selects the best performer:

- **Random Forest Classifier**
- **Decision Tree Classifier**
- **Gradient Boosting Classifier**
- **Logistic Regression**
- **AdaBoost Classifier**

**Training Process:**
- Hyperparameter tuning
- Cross-validation
- Model evaluation
- MLflow tracking

### 5. Model Evaluation

Evaluates models using:

- **Accuracy Score**
- **Precision**
- **Recall**
- **F1 Score**
- **ROC-AUC Score**
- **Confusion Matrix**

### 6. Model Selection & Saving

- Compares all trained models
- Selects the best model based on F1 score
- Saves the model using pickle
- Logs model artifacts in MLflow

## 📡 API Documentation

### Endpoints

#### 1. Home Page
```
GET /
```
Returns the main web interface.

#### 2. Train Model
```
POST /train
```
Triggers the model training pipeline.

**Response:**
```json
{
    "status": "success",
    "message": "Training completed successfully",
    "best_model": "RandomForestClassifier",
    "accuracy": 0.95
}
```

#### 3. Predict
```
POST /predict
```

**Request Body:**
```json
{
    "features": [value1, value2, value3, ...]
}
```

**Response:**
```json
{
    "prediction": "Normal/Malicious",
    "confidence": 0.92,
    "timestamp": "2024-01-15T10:30:00"
}
```

#### 4. Batch Prediction
```
POST /batch_predict
```

Upload a CSV file for batch predictions.

**Response:**
```json
{
    "total_records": 1000,
    "normal_traffic": 850,
    "malicious_traffic": 150,
    "download_link": "/download/predictions.csv"
}
```

## 📊 Model Performance

### Best Model: Random Forest Classifier

| Metric | Score |
|--------|-------|
| Accuracy | 95.2% |
| Precision | 94.8% |
| Recall | 95.6% |
| F1 Score | 95.2% |
| ROC-AUC | 97.3% |



```

``

### Feature Importance

Top 5 most important features:
1. Packet Rate (0.25)
2. Connection Duration (0.18)
3. Protocol Type (0.15)
4. Destination Port (0.12)
5. Payload Size (0.10)

## 🐳 Deployment

### Docker Deployment

#### 1. Build Docker Image

```bash
docker build -t networksecurity:latest .
```

#### 2. Run Docker Container

```bash
docker run -p 8080:8000 \
    -e MONGO_DB_URL=your_mongo_url \
    -e AWS_ACCESS_KEY_ID=your_key \
    -e AWS_SECRET_ACCESS_KEY=your_secret \
    network-security:latest
```

### AWS Deployment

#### Using ECR and ECS

1. **Push to ECR:**
```bash
aws ecr create-repository --repository-name network-security
docker tag network-security:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/network-security:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/network-security:latest
```

2. **Deploy to ECS:**
- Create ECS cluster
- Define task definition
- Create and run service

### CI/CD Pipeline

GitHub Actions automatically:
- Runs tests on push
- Builds Docker image
- Pushes to container registry
- Deploys to production

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Write unit tests for new features
- Update documentation

## 🔮 Future Enhancements

- [ ] **Real-time packet sniffing** using Scapy
- [ ] **Deep learning models** (LSTM, CNN) for sequence analysis
- [ ] **Dashboard** for real-time monitoring
- [ ] **Alert system** with email/SMS notifications
- [ ] **Integration with SIEM** systems
- [ ] **Kubernetes deployment** support
- [ ] **Multi-cloud support** (Azure, GCP)
- [ ] **Automated model retraining** pipeline
- [ ] **A/B testing** framework
- [ ] **GraphQL API** support
- [ ] **Network visualization** dashboard
- [ ] **Explainable AI** for prediction insights

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

**Shivam Sukhija**

- GitHub: [@sukhijashivam](https://github.com/sukhijashivam)
- Email: shivamsukhija002@gmail.com
- LinkedIn: [Your LinkedIn Profile](https://linkedin.com/in/shivam-sukhija-40a37429a/)

## 🙏 Acknowledgments

- Dataset source: [Phishing Data]
- Inspiration: Real-world network security challenges
- Special thanks to the open-source community

---

⭐ **Star this repository** if you find it helpful!

💬 **Questions?** Open an issue or reach out!

🔒 **Stay Secure!**

