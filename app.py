# app.py

import os
import sys
import glob
from datetime import datetime
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import Response, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import certifi
import pymongo
import joblib   # ✅ Added: direct model loading (most reliable)

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.feature_extraction import extract_all_features
from networksecurity.utils.ml_utils.model.estimator import NetworkModel   # IMPORTANT

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
    print("🔍 Loading model...")
    
    # IMPORTANT: import NetworkModel BEFORE loading
    from networksecurity.utils.ml_utils.model.estimator import NetworkModel

    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)

    # Combine model + preprocessor into a NetworkModel wrapper
    network_model = NetworkModel(preprocessor=preprocessor, model=model)

    print("✅ Model Loaded Successfully!")

except Exception as e:
    print("\n❌ ERROR loading model or preprocessor:")
    print(e)
    network_model = None

# ---------------- ROUTES ---------------- #

@app.get("/", tags=["Root"])
async def index():
    return RedirectResponse(url="/upload")


@app.get("/train", tags=["Training"])
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("✅ Training Completed Successfully!")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.get("/upload", tags=["Upload"])
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


# -------- CSV Prediction -------- #

@app.post("/predict", tags=["Prediction"])
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        if not network_model:
            raise HTTPException(status_code=500, detail="Model not loaded.")

        df = pd.read_csv(file.file)

        trained_cols = network_model.preprocessor.feature_names_in_
        df = df.reindex(columns=trained_cols, fill_value=0)

        y_pred = network_model.predict(df)
        df["predicted_column"] = y_pred

        os.makedirs("prediction_output", exist_ok=True)
        output_file = f"prediction_output/output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(output_file, index=False)

        return templates.TemplateResponse("table.html", {"request": request, "df": df})

    except Exception as e:
        raise NetworkSecurityException(e, sys)


# -------- Download Prediction -------- #

@app.get("/download", tags=["Prediction"])
async def download_file():
    try:
        list_of_files = glob.glob("prediction_output/*.csv")
        if not list_of_files:
            raise HTTPException(status_code=404, detail="No prediction files found.")

        latest_file = max(list_of_files, key=os.path.getctime)
        return FileResponse(
            latest_file,
            filename="prediction_results.csv",
            media_type="text/csv",
        )

    except Exception as e:
        raise NetworkSecurityException(e, sys)


# -------- Real-time URL Checker -------- #

@app.get("/check_url", tags=["Real-time URL Check"])
async def check_url(url: str):
    try:
        if not network_model:
            raise HTTPException(status_code=500, detail="Model not loaded.")

        features = extract_all_features(url)
        X = pd.DataFrame([features])
        pred = network_model.predict(X)[0]

        result = "Legitimate" if pred == 1 else "Phishing"

        return {"url": url, "prediction": result, "features": features}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
