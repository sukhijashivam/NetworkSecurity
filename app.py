import sys, os
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import Response, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import pandas as pd
from datetime import datetime
import pymongo
import certifi
import glob
from dotenv import load_dotenv

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.constants.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME,
)

# Load environment variables
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
ca = certifi.where()
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# FastAPI app init
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates folder
templates = Jinja2Templates(directory="templates")

# Root route
@app.get("/", tags=["Root"])
async def index():
    return RedirectResponse(url="/upload")

# Training route
@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("✅ Training Completed Successfully!")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

# Upload page
@app.get("/upload")
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

# Prediction route
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred

        # Save prediction output
        os.makedirs("prediction_output", exist_ok=True)
        output_file = f"prediction_output/output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(output_file, index=False)

        # Return prediction table
        return templates.TemplateResponse("table.html", {"request": request, "df": df})

    except Exception as e:
        raise NetworkSecurityException(e, sys)

# Download latest prediction
@app.get("/download")
async def download_file():
    try:
        list_of_files = glob.glob("prediction_output/*.csv")
        latest_file = max(list_of_files, key=os.path.getctime)
        return FileResponse(latest_file, filename="prediction_results.csv", media_type='text/csv')
    except Exception as e:
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))  # Render sets PORT env variable
    app_run(app, host="0.0.0.0", port=port)


