import os
import sys
from pathlib import Path
from zipfile import ZipFile
from hate_speech.logger import logging
from hate_speech.exception import CustomException
from hate_speech.configuration.gcloud_syncer import GCloudSync
from hate_speech.entity.config_entity import DataIngestionConfig
from hate_speech.entity.artifact_entity import DataIngestionArtifacts



class DataIngestion:
    
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        
        self.data_ingestion_config=data_ingestion_config
        self.gcloud=GCloudSync()
     
        
    def get_data_from_gcloud(self) -> None:
        
        try :
            logging.info("Entered the get_data_from_gcloud method of DataIngestion class in hate_speech/components/data_ingestion.py")
            
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok=True)
            
            self.gcloud.sync_folder_from_gcloud( gcp_bucket_name=self.data_ingestion_config.BUCKET_NAME,
                                    gcs_filename=self.data_ingestion_config.GCP_BUCKET_FILENAME,
                                    destination_dir=self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR,
                                    new_filename= "dataset.zip"
                                    ) 
            
            logging.info("Exited the get_data_from_gcloud method of DataIngestion class in hate_speech/components/data_ingestion.py")
            
        except Exception as e:
            raise CustomException(e,sys) from e
        
    
    def unzip_data(self):
        
        logging.info("Entered the unzip_data method of DataIngestion class in hate_speech/components/data_ingestion.py")
        
        try:
            
            with ZipFile(file=self.data_ingestion_config.DATA_ZIP_FILE_PATH, mode="r") as zip_ref:
                zip_ref.extractall(path=self.data_ingestion_config.DATA_ZIP_FILE_DIR)
                
            logging.info("Exited the unzip_data method of DataIngestion class in hate_speech/components/data_ingestion.py")
            
            # returing a tuple that has imbalance & raw data filepaths
            return (self.data_ingestion_config.DATA_INGESTION_IMBALANCE_DATA_FILEPATH ,
                    self.data_ingestion_config.DATA_INGESTION_RAW_DATA_FILEPATH)

        except Exception as e :
            raise CustomException(e, sys) from e
        
    
    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        
        logging.info("Entered the initiate_data_ingestion method of DataIngestion class in hate_speech/components/data_ingestion.py")
        
        try :
            
            # Calling method 
            self.get_data_from_gcloud()
            logging.info("Fetched the data from GCS bucket.")
            
            imbalance_Data_filepath, raw_data_filepath = self.unzip_data()
            logging.info("Unzipped the data.")
            
            data_ingestion_artifacts=DataIngestionArtifacts(imbalance_data_filepath=imbalance_Data_filepath,
                                                            raw_data_filepath=raw_data_filepath
                                                            )
            
            logging.info("Exited the initiate_data_ingestion method of DataIngestion class in hate_speech/components/data_ingestion.py")
            logging.info(f"Data ingestion artifact : {data_ingestion_artifacts}")
            
            # Returning the object of DataIngestionArtifacts class
            return data_ingestion_artifacts
        
        except Exception as e:
            raise  CustomException(e, sys) from e
            





