import os
import sys
import glob
import pandas as pd
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import Response, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv
import certifi
import pymongo
import joblib

from networksecurity.logging.logger import logger
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.feature_extraction import extract_all_features
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

# ---------------- ENV & MONGO ---------------- #

load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
ca = certifi.where()

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
from networksecurity.constants.training_pipeline import (
    DATA_INGESTION_DATABASE_NAME,
    DATA_INGESTION_COLLECTION_NAME,
)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# ---------------- FASTAPI APP ---------------- #

app = FastAPI(title="Network Security URL Checker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# ---------------- LOAD MODEL ---------------- #

MODEL_PATH = "final_model/model.pkl"
PREPROCESSOR_PATH = "final_model/preprocessor.pkl"

network_model = None
preprocessor = None

try:
    logger.info("Loading model & preprocessor...")

    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)

    network_model = NetworkModel(preprocessor=preprocessor, model=model)

    logger.info("Model loaded successfully!")

except Exception as e:
    logger.error(f"Model loading FAILED: {e}")
    network_model = None

# ---------------- ROUTES ---------------- #

@app.get("/")
async def index():
    logger.info("Root '/' accessed")
    return RedirectResponse(url="/upload")


@app.get("/train")
async def train_route():
    try:
        logger.info("Training started...")
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        logger.info("Training completed successfully!")
        return Response("Training Completed Successfully!")
    except Exception as e:
        logger.error("Training failed!")
        raise NetworkSecurityException(e, sys)


@app.get("/upload")
async def upload_page(request: Request):
    logger.info("Upload page opened")
    return templates.TemplateResponse("upload.html", {"request": request})


# -------- CSV Prediction -------- #

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        logger.info(f"Prediction requested: {file.filename}")

        df = pd.read_csv(file.file)

        trained_cols = network_model.preprocessor.feature_names_in_
        df = df.reindex(columns=trained_cols, fill_value=0)

        y_pred = network_model.predict(df)
        df["predicted_column"] = y_pred

        os.makedirs("prediction_output", exist_ok=True)
        path = f"prediction_output/output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(path, index=False)

        logger.info(f"Prediction completed. Saved to {path}")

        return templates.TemplateResponse("table.html", {"request": request, "df": df})

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise NetworkSecurityException(e, sys)


# -------- Download Prediction -------- #

@app.get("/download")
async def download_file():
    try:
        files = glob.glob("prediction_output/*.csv")
        if not files:
            raise HTTPException(status_code=404, detail="No files found")

        latest_file = max(files, key=os.path.getctime)
        logger.info(f"Downloading file: {latest_file}")

        return FileResponse(latest_file, filename="prediction_results.csv")

    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise NetworkSecurityException(e, sys)


# -------- Real-time URL Checker -------- #

@app.get("/check_url")
async def check_url(url: str):
    try:
        logger.info(f"Real-time URL check: {url}")

        features = extract_all_features(url)
        df = pd.DataFrame([features])

        pred = network_model.predict(df)[0]
        result = "Legitimate" if pred == 1 else "Phishing"

        logger.info(f"URL: {url} | Prediction: {result}")

        return {"url": url, "prediction": result}

    except Exception as e:
        logger.error(f"Real-time URL check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
