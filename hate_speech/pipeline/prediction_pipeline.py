import os ,io , sys, pickle
#from PIL import Image

import keras
from keras.utils import pad_sequences

from hate_speech.logger import logging
from hate_speech.constants import *
from hate_speech.exception import CustomException

from hate_speech.configuration.gcloud_syncer import GCloudSync
from hate_speech.components.data_transformation import DataTransformation
from hate_speech.entity.config_entity import DataTransformationConfig
from hate_speech.entity.artifact_entity import DataIngestionArtifacts



class PredictionPipeline:
    
    def __init__(self):
        
        self.bucket_name = BUCKET_NAME
        self.model_name = MODEL_NAME
        self.model_path = os.path.join("artifacts", "ProductionModel")
        self.gcloud = GCloudSync()
        self.data_transformation = DataTransformation(data_transformation_config= DataTransformationConfig,
                                                      data_ingestion_artifacts=DataIngestionArtifacts)


    
    def get_model_from_gcloud(self) -> str:
        
        """
        Method Name :   get_model_from_gcloud
        Description :   This method to get best/production model from gcloud storage
        Output      :   best_model_path
        """
        
        logging.info("Entered the get_model_from_gcloud method of PredictionPipeline class of hate_speech/pipeline/prediction_pipeline.py")
        
        try:
            
            best_model_path = os.path.join(self.model_path, self.model_name)
            
            if not os.path.exists(best_model_path): 
                
                # Loading the best model from s3 bucket
                os.makedirs(self.model_path, exist_ok=True)
                
                """ 
                Parameters : 
                    (a) gcp_bucket_url: bucket name in the gcp (bucket cloud)
                    (b) filename: name of the file present in the above gcp bucket, filename should match exactly
                    (c) destination: path of the project directory where file being downloaded from the gcp bucket will be saved inside.
                """
                self.gcloud.sync_folder_from_gcloud(gcp_bucket_url=self.bucket_name,
                                                    filename=self.model_name,
                                                    destination=self.model_path)
            
            # best_model_path = os.path.join(self.model_path, self.model_name)
            
            logging.info("Exited the get_model_from_gcloud method of PredictionPipeline class")
            
            return best_model_path

        except Exception as e:
            raise CustomException(e, sys) from e
        
 
    def predict(self,best_model_path,input_text):
        
        
        logging.info("Running the predict method inside PredictionPipeline class of hate_speech/pipeline/prediction_pipeline.py")
        
        try:
            
            # Calling method
            #best_model_path:str = self.get_model_from_gcloud()
            # Best/Production model used for custom input text prediction for hate or no-hate
            best_model=keras.models.load_model(best_model_path)
            
            with open('tokenizer.pickle', 'rb') as handle:
                load_tokenizer = pickle.load(handle)
            
            text=self.data_transformation.concat_df_data_cleaning(input_text)
            text = [text]              
            print("Custom Input text to the best model : \n",text)
            
            seq = load_tokenizer.texts_to_sequences(text)
            seq_padded = pad_sequences(seq, maxlen=MAX_LEN)
            print("Padded sequence : \n",seq_padded)
            
            pred = best_model.predict(seq_padded)
            # pred
            print("Model prediction on custom text input : ", pred)
            
            if pred>0.5:

                print("hate and abusive")
                return "hate and abusive"
            else:
                print("no hate")
                return "no hate"
            
        except Exception as e:
            raise CustomException(e, sys) from e

    
    def run_pipeline(self,text):
        
        logging.info("Entered the run_pipeline method of PredictionPipeline class of hate_speech/pipeline/prediction_pipeline.py")
        
        try:

            # Calling methods    
            Best_model_path = self.get_model_from_gcloud() 
            predicted_result = self.predict(best_model_path=Best_model_path,
                                            input_text=text)
            
            
            logging.info("Exited the run_pipeline method of PredictionPipeline class")
            
            return predicted_result
        
        except Exception as e:
            raise CustomException(e, sys) from e



