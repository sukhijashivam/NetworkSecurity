# 🛡️ Network Security - ML Project

Machine learning project for detecting network intrusions and anomalous traffic patterns.

## 📋 About

An end-to-end ML pipeline that analyzes network traffic to identify potential security threats using machine learning algorithms. The system processes network data, trains multiple models, and provides real-time predictions through a web API.

**Key Features:**
- 🔍 **Anomaly Detection** - Identifies unusual network traffic patterns
- 📊 **Multiple ML Models** - Random Forest, Decision Tree, Gradient Boosting
- 🔄 **Automated Pipeline** - Complete MLOps workflow
- 🌐 **REST API** - Flask-based prediction service
- 💾 **MongoDB Integration** - Scalable data storage
- 📈 **Experiment Tracking** - MLflow for model versioning
- 🐳 **Docker Support** - Containerized deployment
- ☁️ **Cloud Ready** - AWS S3 integration

## 🛠️ Tech Stack

- **Python 3.8+**
- **Scikit-learn** - Machine learning algorithms
- **Flask** - Web framework & REST API
- **MongoDB** - NoSQL database
- **MLflow** - Experiment tracking
- **AWS S3** - Cloud storage
- **Docker** - Containerization
- **Imbalanced-learn** - Handling imbalanced datasets

## 📁 Project Structure

```
NetworkSecurity/
│
├── networksecurity/            # Main package
│   ├── components/             # Pipeline components
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   └── model_evaluation.py
│   ├── entity/                 # Data classes
│   ├── pipeline/               # Training & prediction pipelines
│   ├── utils/                  # Utility functions
│   ├── logging/                # Custom logging
│   └── exception/              # Custom exceptions
│
├── Network_Data/               # Raw datasets
├── final_model/                # Trained models
├── mlruns/                     # MLflow tracking
├── templates/                  # Web UI templates
│
├── app.py                      # Flask application
├── main.py                     # Training pipeline
├── push_data.py                # Data ingestion
├── requirements.txt            # Dependencies
├── Dockerfile                  # Docker config
└── setup.py                    # Package setup
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- MongoDB (local or Atlas)
- AWS Account (optional, for S3 storage)

### Setup Steps

**1. Clone the repository**
```bash
git clone https://github.com/sukhijashivam/NetworkSecurity.git
cd NetworkSecurity
```

**2. Create virtual environment**
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

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
```

**5. Install the package**
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

### 3. Start Web Application
```bash
python app.py
```
Access at: `http://localhost:5000`

### 4. Make Predictions via API
```python
import requests

# Prepare data
data = {
    'features': [value1, value2, value3, ...]
}

# Get prediction
response = requests.post(
    'http://localhost:5000/predict',
    json=data
)

print(response.json())
```

## 🔄 ML Pipeline

### Pipeline Stages

1. **Data Ingestion**
   - Fetches network traffic data from MongoDB
   - Validates data format and schema
   - Stores raw data for processing

2. **Data Validation**
   - Checks for missing values
   - Validates data types
   - Ensures data quality standards

3. **Data Transformation**
   - Feature engineering
   - Handles imbalanced datasets using SMOTE
   - Scaling and normalization
   - Train-test split

4. **Model Training**
   - Trains multiple ML algorithms
   - Hyperparameter tuning
   - Cross-validation
   - MLflow experiment tracking

5. **Model Evaluation**
   - Compares model performance
   - Evaluates using multiple metrics
   - Selects best performing model

6. **Model Deployment**
   - Saves the best model
   - Registers in MLflow
   - Ready for predictions

## 📡 API Documentation

### Endpoints

#### Home Page
```
GET /
```
Returns the web interface.

#### Train Model
```
POST /train
```
Triggers the model training pipeline.

**Response:**
```json
{
    "status": "success",
    "message": "Training completed",
    "best_model": "RandomForestClassifier"
}
```

#### Predict
```
POST /predict
```

**Request:**
```json
{
    "features": [value1, value2, value3, ...]
}
```

**Response:**
```json
{
    "prediction": "Normal/Malicious",
    "confidence": 0.92
}
```

#### Batch Prediction
```
POST /batch_predict
```
Upload CSV file for batch predictions.

## 📊 Model Performance

### Trained Models

| Model | Accuracy | Precision | Recall | F1 Score |
|-------|----------|-----------|--------|----------|
| Random Forest | 95.2% | 94.8% | 95.6% | 95.2% |
| Gradient Boosting | 94.1% | 93.7% | 94.5% | 94.0% |
| Decision Tree | 91.5% | 90.9% | 92.1% | 91.3% |

### Best Model: Random Forest Classifier
- **Accuracy:** 95.2%
- **F1 Score:** 95.2%
- **ROC-AUC:** 97.3%

## 🐳 Docker Deployment

### Build and Run

**Build Docker image**
```bash
docker build -t networksecurity:latest .
```

**Run container**
```bash
docker run -p 8080:8000 \
  -e MONGO_DB_URL=your_mongo_url \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  networksecurity:latest
```

### AWS Deployment

**Push to ECR**
```bash
aws ecr create-repository --repository-name networksecurity
docker tag networksecurity:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/networksecurity:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/networksecurity:latest
```

## 🔮 Future Enhancements

- [ ] Real-time packet sniffing using Scapy
- [ ] Deep learning models (LSTM, CNN)
- [ ] Dashboard for real-time monitoring
- [ ] Alert system with notifications
- [ ] Kubernetes deployment support
- [ ] Multi-cloud support (Azure, GCP)
- [ ] Automated model retraining

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚠️ Note

This is an educational project for learning MLOps concepts and network security fundamentals. Not intended for production use without proper security audits.

## 👨‍💻 Author

**Shivam Sukhija**
- GitHub: [@sukhijashivam](https://github.com/sukhijashivam)
- Email: shivamsukhija002@gmail.com
- LinkedIn: [Shivam Sukhija](https://linkedin.com/in/shivam-sukhija-40a37429a/)

## 📄 License

MIT License - feel free to use this project for learning and development.

## 🙏 Acknowledgments

- Scikit-learn and Flask communities
- MLflow for experiment tracking
- MongoDB for database support

---

⭐ If you find this project helpful, please star the repository!
