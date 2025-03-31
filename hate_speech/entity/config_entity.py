from dataclasses import dataclass
from hate_speech.constants import *
import os
from pathlib import Path


@dataclass
class DataIngestionConfig:
    
    def __init__(self):
        
        self.BUCKET_NAME=BUCKET_NAME      # glcoud bucket name
        self.ZIP_FILE_NAME=ZIP_FILENAME  # Name of the file inside gcloud bucket
        self.DATA_INGESTION_ARTIFACTS_DIR:str = Path(os.path.join(os.getcwd(), ARTIFACTS_DIR, DATA_INGESTION_ARTIFACT_DIR) )
        
        # we need to change the name of the attributes( its quite confusing)
        self.DATA_ARTIFACTS_DIR:str = Path(os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_IMBALANCE_DATA_DIR ) )
        self.NEW_DATA_ARTIFACTS_DIR:str= Path(os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_RAW_DATA_DIR) )
        
        self.ZIP_FILE_DIR= Path(os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR) )
        self.ZIP_FILE_PATH= Path(os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR, self.ZIP_FILE_NAME))
        
        
@dataclass
class DataTransformationConfig:
    
    def __init__(self):
        
        self.DATA_TRANSFORMATION_ARTIFACTS_DIR:str=os.path.join(os.getcwd(), ARTIFACTS_DIR, DATA_TRANSFORMATION_ARTIFACTS_DIR)
        self.TRANSFORMED_FILEPATH=os.path.join(self.DATA_TRANSFORMATION_ARTIFACTS_DIR,TRANSFORMED_FILENAME)
        self.ID=ID
        self.AXIS=AXIS
        self.INPLACE=INPLACE
        self.DROP_COLUMNS=DROP_COLUMNS
        self.CLASS=CLASS
        self.LABEL=LABEL
        self.TWEET=TWEET
        







