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
            
            self.gcloud.sync_folder_from_gcloud(gcp_bucket_url=self.data_ingestion_config.BUCKET_NAME,
                                    filename=self.data_ingestion_config.ZIP_FILE_NAME,
                                    destination=self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR
                                               )
            #destination_path= Path(r"E:/STUDY/NLP/Projects/DS bappy/hate_speech_classification/artifacts/Mar_24_2025_18_35_49/DataIngestionArtifacts")
            #destination_path= "E:/STUDY/NLP/Projects/DS bappy/hate_speech_classification/artifacts/Mar_24_2025_18_35_49/DataIngestionArtifacts"
            #destination_path= r"E:/STUDY/NLP/Projects/DS bappy"

            # self.gcloud.sync_folder_from_gcloud(gcp_bucket_url=self.data_ingestion_config.BUCKET_NAME,
            #                         filename=self.data_ingestion_config.ZIP_FILE_NAME,
            #                         destination=destination_path
            #                                    )
            # E:\STUDY\NLP\Projects\DS bappy\hate_speech_classification\artifacts\Mar_24_2025_18_35_49\DataIngestionArtifacts
            
            
            logging.info("Exited the get_data_from_gcloud method of DataIngestion class in hate_speech/components/data_ingestion.py")
            
        except Exception as e:
            raise CustomException(e,sys) from e
        
    
    def unzip_and_clean(self):
        
        logging.info("Entered the unzip_and_clean method of DataIngestion class in hate_speech/components/data_ingestion.py")
        
        try:
            
            with ZipFile(file=self.data_ingestion_config.ZIP_FILE_PATH, mode="r") as zip_ref:
                zip_ref.extractall(path=self.data_ingestion_config.ZIP_FILE_DIR)
                
            logging.info("Exited the unzip_and_clean method of DataIngestion class in hate_speech/components/data_ingestion.py")
            
            return self.data_ingestion_config.DATA_ARTIFACTS_DIR , self.data_ingestion_config.NEW_DATA_ARTIFACTS_DIR

        except Exception as e :
            raise CustomException(e, sys) from e
        
    
    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        
        logging.info("Entered the initiate_data_ingestion method of DataIngestion class in hate_speech/components/data_ingestion.py")
        
        try :
            
            self.get_data_from_gcloud()
            logging.info("Fetched the data from gcloud bucket.")
            
            imbalance_Data_filepath, raw_data_filepath = self.unzip_and_clean()
            logging.info("Unzipped the data.")
            
            data_ingestion_artifacts=DataIngestionArtifacts(imbalance_data_file_path=imbalance_Data_filepath,
                                                            raw_data_file_path=raw_data_filepath
                                                            )
            
            logging.info("Exited the initiate_data_ingestion method of DataIngestion class in hate_speech/components/data_ingestion.py")
            logging.info(f"Data ingestion artifact : {data_ingestion_artifacts}")
            
            # Returning the object of DataIngestionArtifacts class
            return data_ingestion_artifacts
        
        except Exception as e:
            raise  CustomException(e, sys) from e
            











