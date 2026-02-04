
import os
import subprocess
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import sys


class S3Sync:
    def sync_folder_to_s3(self,folder,aws_bucket_url):
        try:
            command = f"aws s3 sync {folder} {aws_bucket_url} "
            logging.info(f"Executing S3 sync command: {command}")
            
            # Check if folder exists
            if not os.path.exists(folder):
                logging.warning(f"Folder does not exist: {folder}")
                return
            
            # Run command and capture output
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                logging.error(f"S3 sync failed: {result.stderr}")
            else:
                logging.info(f"Successfully synced {folder} to {aws_bucket_url}")
                logging.info(f"S3 sync output: {result.stdout}")
        except Exception as e:
            logging.error(f"Error during S3 sync: {str(e)}")

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        try:
            command = f"aws s3 sync {aws_bucket_url} {folder} "
            logging.info(f"Executing S3 sync command: {command}")
            
            # Create folder if it doesn't exist
            os.makedirs(folder, exist_ok=True)
            
            # Run command and capture output
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                logging.error(f"S3 sync failed: {result.stderr}")
            else:
                logging.info(f"Successfully synced {aws_bucket_url} to {folder}")
                logging.info(f"S3 sync output: {result.stdout}")
        except Exception as e:
            logging.error(f"Error during S3 sync: {str(e)}")
