# networksecurity/utils/ml_utils/model/model_loader.py

import os
import sys
import joblib
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
from networksecurity.exception.exception import NetworkSecurityException

def load_model(model_path: str = None) -> NetworkModel:
    try:
        if model_path is None:
            model_path = os.path.join(SAVED_MODEL_DIR, MODEL_FILE_NAME)

        preprocessor_path = os.path.join(SAVED_MODEL_DIR, "preprocessor.pkl")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        if not os.path.exists(preprocessor_path):
            raise FileNotFoundError(f"Preprocessor file not found at: {preprocessor_path}")

        preprocessor = joblib.load(preprocessor_path)
        model = joblib.load(model_path)

        return NetworkModel(preprocessor=preprocessor, model=model)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
