import sys
from hate_speech.logger import logging
from hate_speech.exception import CustomException
from hate_speech.components.data_ingestion import DataIngestion
from hate_speech.components.data_transformation import DataTransformation

from hate_speech.entity.config_entity import (DataIngestionConfig,
                                              DataTransformationConfig)

from hate_speech.entity.artifact_entity import (DataIngestionArtifacts,
                                                DataTransformationArtifacts)




class TrainPipeline:
    
    def __init__(self):
        
        self.data_ingestion_config=DataIngestionConfig()
        self.data_transformation_config=DataTransformationConfig()
        
        
    
    def start_data_ingestion(self) -> DataIngestionArtifacts :
        
        logging.info("Entered the start_data_ingestion method of TrainPipeline class in hate_speech/pipeline/train_pipeline.py")
        
        try:
            logging.info("Geting the dta from GCLOUD Storage bucket")
            
            # Creating the object of the class DataIngestion
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            
            # returing the DataIngestionArtifacts class object as data_ingestion_artifacts
            data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
            
            logging.info("Exited the start_data_ingestion method of TrainPipeline class in hate_speech/pipeline/train_pipeline.py")
        
            return data_ingestion_artifacts
        
        except Exception as e :
            raise CustomException(e, sys) from e
        
        
    def start_data_transformation(self, data_ingestion_artifacts:DataIngestionArtifacts) -> DataTransformationArtifacts:
        
        logging.info("Entered the start_data_transformation method of TrainPipeline class in hate_speech/pipeline/train_pipeline.py")
        
        try :
            
            data_transformation=DataTransformation(
                                        data_ingestion_artifacts=data_ingestion_artifacts, 
                                        data_transformation_config=self.data_transformation_config,    
                                        )
            
            data_transformation_artifacts=data_transformation.initiate_data_transformation()
            
            logging.info(f"Exited the start_data_transformation method of TrainPipeline class.")
            
            return data_transformation_artifacts
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
        
    def run_pipeline(self):
        
        logging.info("Entered the run_pipline method of TrainPipeline class in hate_speech/pipeline/train_pipeline.py")
        
        try:
            data_ingestion_artifacts=self.start_data_ingestion()
            
            data_transformation_artifacts=self.start_data_transformation(
                        data_ingestion_artifacts=data_ingestion_artifacts
                        )
            
            
            logging.info("Exited the run_pipline method of TrainPipeline class in hate_speech/pipeline/train_pipeline.py")
            
        except Exception as e:
            
            raise  CustomException(e, sys) from e
        
            









