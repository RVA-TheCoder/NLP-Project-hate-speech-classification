from dataclasses import dataclass
from hate_speech.constants import *
import os
from pathlib import Path


@dataclass
class DataIngestionConfig:
    
    def __init__(self):
        
        self.BUCKET_NAME=BUCKET_NAME      # glcoud bucket name
        self.GCP_BUCKET_FILENAME=GCP_BUCKET_FILENAME  # Name of the file inside gcloud bucket
        
        self.DATA_INGESTION_ARTIFACTS_DIR:str = Path(os.path.join(os.getcwd(), 
                                                                  ARTIFACTS_DIR,
                                                                  DATA_INGESTION_ARTIFACT_DIR 
                                                                 ) 
                                                     )
        
        self.DATA_INGESTION_IMBALANCE_DATA_FILEPATH:str = Path(os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR,
                                                        DATA_INGESTION_IMBALANCE_DATA_FILENAME ) 
                                                        )
        
        self.DATA_INGESTION_RAW_DATA_FILEPATH:str= Path(os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR,
                                                           DATA_INGESTION_RAW_DATA_FILENAME) 
                                                       )
        
        self.DATA_ZIP_FILE_DIR= Path(os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR) 
                                )
        
        self.DATA_ZIP_FILE_PATH= Path(os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR, 
                                              self.GCP_BUCKET_FILENAME)
                                 )
        
        
@dataclass
class DataTransformationConfig:
    
    def __init__(self):
        
        self.DATA_TRANSFORMATION_ARTIFACTS_DIR:str=os.path.join(os.getcwd(), 
                                                                ARTIFACTS_DIR,
                                                                DATA_TRANSFORMATION_ARTIFACTS_DIR
                                                                )
       
        self.TRANSFORMED_DATA_FILEPATH=os.path.join(self.DATA_TRANSFORMATION_ARTIFACTS_DIR,
                                                    TRANSFORMED_DATA_FILENAME)
        self.ID=ID
        self.AXIS=AXIS
        self.INPLACE=INPLACE
        self.DROP_COLUMNS=DROP_COLUMNS
        self.CLASS=CLASS
        self.LABEL=LABEL
        self.TWEET=TWEET
        


@dataclass
class ModelTrainerConfig:
    
    def __init__(self):
        
        self.TRAINED_MODEL_DIR:str=os.path.join(os.getcwd(),
                                                ARTIFACTS_DIR,
                                                MODEL_TRAINER_ARTIFACTS_DIR)
        
        self.TRAINED_MODEL_PATH=os.path.join(self.TRAINED_MODEL_DIR, TRAINED_MODEL_NAME)
        
        self.X_TRAIN_DATA_PATH=os.path.join(self.TRAINED_MODEL_DIR, X_TRAIN_FILENAME)
        
        self.X_TEST_DATA_PATH=os.path.join(self.TRAINED_MODEL_DIR, X_TEST_FILENAME)
        self.Y_TEST_DATA_PATH=os.path.join(self.TRAINED_MODEL_DIR, Y_TEST_FILENAME)
        
        
        self.MAX_WORDS=MAX_WORDS
        self.MAX_LEN=MAX_LEN
        self.LOSS=LOSS
        
        self.METRICS=METRICS
        self.ACTIVATION=ACTIVATION
        self.LABEL=LABEL
        self.TWEET=TWEET
        self.RANDOM_STATE=RANDOM_STATE
        self.EPOCH=EPOCH
        self.BATCH_SIZE=BATCH_SIZE
        self.VALIDATION_SPLIT=VALIDATION_SPLIT
        
        
@dataclass
class ModelEvaluationConfig:
    
    def __init__(self):
        
        self.MODEL_EVALUATION_MODEL_DIR : str = os.path.join(os.getcwd(),
                                                             ARTIFACTS_DIR,
                                                             MODEL_EVALUATION_ARTIFACTS_DIR)
        
        self.GCS_MODEL_DIR_PATH : str = os.path.join(self.MODEL_EVALUATION_MODEL_DIR, GCS_MODEL_DIR)
        
        self.BUCKET_NAME= BUCKET_NAME
        self.MODEL_NAME= MODEL_NAME
        


@dataclass
class ModelPusherConfig:
    
    def __init__(self):
        
        self.TRAINED_MODEL_DIR_PATH=os.path.join( os.getcwd(),
                                             ARTIFACTS_DIR,
                                             MODEL_TRAINER_ARTIFACTS_DIR
                                             )
        
        self.BUCKET_NAME=BUCKET_NAME
        self.MODEL_NAME=MODEL_NAME
        
        
        



