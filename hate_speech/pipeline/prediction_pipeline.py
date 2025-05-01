import os, io, sys, pickle
#from PIL import Image

import keras
from keras.utils import pad_sequences

from hate_speech.logger import logging
from hate_speech.constants import *
from hate_speech.exception import CustomException

from hate_speech.components.data_transformation import DataTransformation

from hate_speech.entity.config_entity import DataTransformationConfig
from hate_speech.entity.artifact_entity import DataIngestionArtifacts



class PredictionPipeline:
    
    def __init__(self):
        
        self.model_name = MODEL_NAME
        self.production_model_path = os.path.join("ProductionModel", MODEL_NAME)
        
        self.data_transformation = DataTransformation(data_ingestion_artifacts=DataIngestionArtifacts,
                                                      data_transformation_config=DataTransformationConfig,
                                                      )
    
 
    def predict(self, input_text):
        
        
        logging.info("Running the predict method inside PredictionPipeline class of hate_speech/pipeline/prediction_pipeline.py")
        
        try:
            
            production_model=keras.models.load_model(self.production_model_path)
            
            with open('tokenizer.pickle', 'rb') as handle:
                tokenizer = pickle.load(handle)
            
            # Preprocessing the input text
            text=self.data_transformation.concat_df_text_preprocessing(input_text)
            text = [text]              
            print("Custom Input text to the best model : \n",text)
            
            # Tokenizing the text
            seq = tokenizer.texts_to_sequences(text)
            seq_padded = pad_sequences(seq, maxlen=MAX_LEN)
            print("Padded sequence : \n",seq_padded)
            
            pred = production_model.predict(seq_padded)
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

    
    def run_pipeline(self, text):
        
        logging.info("Entered the run_pipeline method of PredictionPipeline class of hate_speech/pipeline/prediction_pipeline.py")
        
        try:

            # Calling methods    
            predicted_result = self.predict( input_text=text )
                                            
            logging.info("Exited the run_pipeline method of PredictionPipeline class")
            
            return predicted_result
        
        except Exception as e:
            
            raise CustomException(e, sys) from e



