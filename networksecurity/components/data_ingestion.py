import sys
import os
import pandas as pd

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        """
        Reads the dataset directly from CSV file instead of MongoDB.
        """
        try:
            logging.info(f"Reading dataset from CSV: {self.data_ingestion_config.dataset_file_path}")
            df = pd.read_csv(self.data_ingestion_config.dataset_file_path)
            logging.info(f"Dataset loaded successfully with shape: {df.shape}")
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion process...")

            df = self.export_collection_as_dataframe()

            # Create directories
            os.makedirs(self.data_ingestion_config.ingested_dir, exist_ok=True)

            # Save train.csv and test.csv
            train_df = df.sample(frac=0.8, random_state=42)
            test_df = df.drop(train_df.index)

            train_file_path = self.data_ingestion_config.train_file_path
            test_file_path = self.data_ingestion_config.test_file_path

            train_df.to_csv(train_file_path, index=False)
            test_df.to_csv(test_file_path, index=False)

            logging.info(f"Train file saved at: {train_file_path}")
            logging.info(f"Test file saved at: {test_file_path}")

            # Create artifact object
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=train_file_path,
                test_file_path=test_file_path
            )

            logging.info("Data ingestion completed successfully.")
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

