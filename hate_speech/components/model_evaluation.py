import os, sys, pickle

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

import keras
from keras.utils import pad_sequences

from hate_speech.logger import logging
from hate_speech.exception import CustomException


from hate_speech.constants import *
from hate_speech.configuration.gcloud_syncer import GCloudSync


from hate_speech.entity.config_entity import ModelEvaluationConfig
from hate_speech.entity.artifact_entity import (ModelEvaluationArtifacts,
                                                ModelTrainerArtifacts,
                                                DataTransformationArtifacts)


class ModelEvaluation:
    
    def __init__(self, 
                 model_evaluation_config : ModelEvaluationConfig,
                 model_trainer_artifacts:ModelTrainerArtifacts,
                 data_transformation_artifacts:DataTransformationArtifacts) :
        
        self.model_evaluation_config=model_evaluation_config
        self.model_trainer_artifacts = model_trainer_artifacts
        self.data_transformation_artifacts=data_transformation_artifacts
        self.gcloud=GCloudSync()
        
        
    def get_best_model_from_gcloud(self) -> str :
        
        """
        return : fetch the best model from gcloud bucket storage and store inside best model directory path
        """
        
        try : 
            
            logging.info("Entered the get_best_model_from_gcloud method of ModelEvaluation class inside hate_speech/components/model_evaluation.py")
            
            # Making directory named 'ModelEvaluationArtifacts/best_model/' for the best model(production model) 
            os.makedirs(self.model_evaluation_config.BEST_MODEL_DIR_PATH, exist_ok=True)
            
            """
            Parameters : 
            (a) gcp_bucket_url: bucket name in the gcp (bucket cloud)
            (b) filename: name of the file present in the above gcp bucket, filename should match exactly
            (c) destination: path of the project directory where file being downloaded from the gcp bucket will be saved inside.
                
            """
            self.gcloud.sync_folder_from_gcloud(gcp_bucket_url=self.model_evaluation_config.BUCKET_NAME,
                                                filename=self.model_evaluation_config.MODEL_NAME,
                                                destination=self.model_evaluation_config.BEST_MODEL_DIR_PATH
                                                )
            
            best_model_path = os.path.join(self.model_evaluation_config.BEST_MODEL_DIR_PATH,
                                           self.model_evaluation_config.MODEL_NAME)
            
            logging.info("Exited the get_best_model_from_gcloud method of ModelEvaluation class.")
            
            return best_model_path
        
        except Exception as e :
            
            raise CustomException(e, sys) from e
        
        
    def evaluate(self, loaded_model):
        
        """
        returns test accuracy metric
        """
        try :
            
            logging.info("Entered the evaluate method  of ModelEvaluation class inside hate_speech/components/model_evaluation.py")
            print(self.model_trainer_artifacts.x_test_path)
            
            x_test=pd.read_csv(self.model_trainer_artifacts.x_test_path,
                               index_col=0)
            print(x_test.head())
            
            y_test=pd.read_csv(self.model_trainer_artifacts.y_test_path,
                               index_col=0)
            print(y_test.head())
            
            
            with open('tokenizer.pickle','rb') as handle:
                
                tokenizer=pickle.load(handle)
                
            #loaded_model=keras.models.load_model(self.model_trainer_artifacts.trained_model_path)
            
            x_test=x_test['tweet'].astype(str)
            
            x_test = x_test.squeeze()
            y_test = y_test.squeeze()
            
            print(f"x_test shape : {x_test.shape}\n")
            print(f"y_test shape : {y_test.shape}")
            
            test_sequences=tokenizer.texts_to_sequences(x_test)
            test_sequences_matrix=pad_sequences(test_sequences, maxlen=MAX_LEN)
            
            
            print(f"-------------test_sequences_matrix-------------\n",test_sequences_matrix,"\n\n\n\n")  
                     
            test_accuracy=loaded_model.evaluate(test_sequences_matrix, y_test)
            
            logging.info(f"The test accuracy : {test_accuracy}")
            
            lstm_predictions= loaded_model.predict(test_sequences_matrix)
            
            res=[]
            for pred in lstm_predictions:
                
                if pred[0] < 0.5 :
                    res.append(0)  # 0 -> no hate speech
                    
                else :
                    res.append(1)  # 1 -> hate speech
                    
            conf_matrix = confusion_matrix(y_test,res)
            print(f"confusion matrix on test data : \n {conf_matrix}")
            
            logging.info(f"the confusion matrix : {conf_matrix}")
            
            return test_accuracy
           
        except Exception as e :
            
            raise CustomException(e,sys) from e

    def initiate_model_evaluation(self) -> ModelEvaluationArtifacts :
        
        """
        method name : initiate_model_evaluation
        Description : This function is used to initiate all steps of the model evaluation
        Output : returns model evaluation artifact
        on failure : write an exception log and then raise an exception.
        
        Note : We will push the trained model to the gcloud as our Production model iff best/production 
               model accuracy is less than the trained model accuracy using is_model_accepted bool parameter
        """
        
        logging.info("Initiate Model Evaluation")
        
        try:
            
            logging.info("Loading currently trained model")
            
            trained_model=keras.models.load_model(self.model_trainer_artifacts.trained_model_path)
            
            with open('tokenizer.pickle','rb') as handle:
                
                load_tokenizer=pickle.load(handle)
            
            # Calling evaluate method
            trained_model_accuracy=self.evaluate(loaded_model=trained_model)
            print(f"Trained model accuracy : {trained_model_accuracy}")
            
            logging.info("fetching the best/production model from gcloud bucket storage")
            
            best_model_path=self.get_best_model_from_gcloud()
            
            logging.info("Checking if best/production model is present in the gcloud bucket storage or not ?")
            
            # this checks whether best/production model is present in the gcloud or not.
            #if os.path.isfile(best_model_path) is False:
            if not os.path.isfile(best_model_path):
                
                # No model is present in the gcloud bucket storage.
                # Therefore we need to push the current trained model to gloud.
                is_model_accepted = True
                
                logging.info("No model is present in the gcloud bucket storage.Therefore need to push the current trained model to gloud.")
            
            else:
                
                logging.info("Load the best model fetched from gcloud storage")
                
                best_loaded_model= keras.models.load_model(best_model_path)
                
                best_loaded_model_accuracy = self.evaluate(loaded_model=best_loaded_model)
                print(f"Best/Production model accuracy : {best_loaded_model_accuracy}")
                
                logging.info("Comparing the accuracy on test data using trained and best/production model.")
                
                if best_loaded_model_accuracy > trained_model_accuracy :
                    
                    print("Best/Production model accuracy is more than trained model accuracy.")
                    is_model_accepted = False
                    
                    logging.info("Trained model not accepted")
                    
                else :
                    print("Best/Production model accuracy is lower than trained model accuracy.")
                    is_model_accepted = True 
                    logging.info("Trained model accepted")
                    
            model_evaluation_artifacts = ModelEvaluationArtifacts(is_model_accepted=is_model_accepted)
            
            logging.info("Returning the ModelEvaluationArtifacts")
                    
            return model_evaluation_artifacts
        
        except Exception as e :
            
            raise CustomException(e, sys) from e
                
            
            
            
        
        
        














