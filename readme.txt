Network Security System

1. PROJECT OVERVIEW

The Network-Security project is built to help students and professionals understand how network attacks occur and how security systems detect them.
It includes:

Sending / receiving network packets

Capturing and logging network traffic

Analysing malicious vs normal traffic

Detecting anomalies using Python models

Using a structured project pipeline similar to real-world security systems

The project follows a modular architecture containing data ingestion, data transformation, model training, prediction, and logging.

You can run this project on any system with Python 3 installed.

2. TECHNOLOGIES USED

Python 3

Scapy – packet generation & sniffing

Pandas / NumPy – analytics

Machine Learning / Rule-based detection (if implemented)

Flask / Streamlit (if app.py runs UI)

Logging Modules

YAML Configurations

MongoDB (optional) – used in test_mongodb.py

3. PROJECT FOLDER STRUCTURE
Network-Security/
│
├── Network_Data/              → Contains raw network traffic datasets or sample attack data
├── data_schema/               → Contains data schema JSONs for validation
├── final_model/               → Contains the trained detection model (if ML-based)
├── logs/                      → Stores all system and process logs
├── networksecurity/           → Main module containing project source code
├── prediction_output/         → Saves prediction results
├── templates/                 → Frontend templates if running web-app
├── valid_data/                → Clean or verified data used in processing
│
├── app.py                     → Optional: Web interface or API script
├── main.py                    → MAIN EXECUTION FILE for the entire project pipeline
├── push_data.py               → Pushes data/packets into system or DB
├── test_mongodb.py            → Connectivity script for MongoDB database
│
├── requirements.txt           → All project dependencies
├── setup.py                   → Setup configuration for packaging
└── README.txt                 → This document

4. HOW THE PROJECT WORKS (STEP-BY-STEP DESCRIPTION)
 4.1 Data Ingestion

Raw network traffic data (normal + attack) is stored in Network_Data/

The project reads these datasets using Python

A validation schema in data_schema/ checks:

Required columns

Data types

Missing values

Traffic patterns

4.2 Data Transformation

The data is cleaned, filtered, and converted into numerical form

Noise removal

Feature creation (packet rate, flag counts, source IP analysis)

Scaling / normalization

Transformed output stored in /valid_data

4.3 Model Training 

The system trains security models such as:

Random Forest

Decision Tree

Gradient Boosting

Logistic Regression

AdaBoost

The model with highest accuracy is selected and saved inside /final_model/.

4.4 Prediction Pipeline

Incoming network data is passed through the pipeline

Model predicts normal or malicious behavior

Output saved to /prediction_output/

4.5 Logging

All processing steps generate logs inside /logs/, including:

Errors

Warnings

Attack detection activity

Pipeline execution steps

5. INSTALLATION INSTRUCTIONS
5.1 Clone the Repository
git clone <Repo link>
cd Network-Security

5.2 Install Requirements
pip install -r requirements.txt

5.3 (Optional) Create Virtual Environment
python -m venv venv
source venv/bin/activate   (Linux/Mac)
venv\Scripts\activate      (Windows)

6. EXECUTION GUIDE
6.1 To Run the Main Project Pipeline
python main.py


This automatically performs:

Data ingestion

Data validation

Data transformation

Model prediction or training

Log generation

6.2 To Run the Application (if app.py is a UI)
python app.py

6.3 To Push Data into the System
python push_data.py

6.4 To Test Database Connectivity
python test_mongodb.py

7. IMPORTANT FILES EXPLAINED
main.py

Runs the full workflow

Connects all components

Generates logs and outputs

app.py

Provides a UI or API

Displays prediction results

Accepts file uploads

push_data.py

Sends data packets

Useful for testing live predictions

test_mongodb.py

Checks MongoDB connection

Helps verify database pipeline

Network_Data/

Contains all sample attack datasets (e.g., SYN flood, ICMP flood)

data_schema/

Validates input structure to prevent processing errors

prediction_output/

Stores the system's predictions (attack or normal)

final_model/

Saved machine-learning model after training

8. HOW TO USE THE PROJECT

Prepare dataset inside Network_Data/

Run main.py to train or predict

Check output in:

logs/ → all runtime logs

prediction_output/ → attack/normal results

final_model/ → best performing model

For web-app usage:

Start app.py

Upload data

Read predictions on the screen

9. FUTURE ENHANCEMENTS

Real-time packet sniffing using Scapy

Integration with firewalls (iptables)

Attack simulation dashboard

Deep-learning anomaly detection models

Live network visualisation

10. AUTHOR

Developer: Shivam Sukhija 
Project: Network-Security


