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
                 model_evaluation_config:ModelEvaluationConfig,
                 model_trainer_artifacts:ModelTrainerArtifacts,
                 data_transformation_artifacts:DataTransformationArtifacts) :
        
        
        self.model_evaluation_config=model_evaluation_config
        self.model_trainer_artifacts = model_trainer_artifacts
        self.data_transformation_artifacts=data_transformation_artifacts
        self.gcloud=GCloudSync()
          
        
    def get_best_model_from_gcloud(self) -> str :
        
        """
        Returns : fetch the best model from gcloud bucket storage and store inside best model directory path
        """
        
        try : 
            
            logging.info("Entered the get_best_model_from_gcloud method of ModelEvaluation class inside hate_speech/components/model_evaluation.py")
            
            # Making directory named 'ModelEvaluationArtifacts/best_model/' for the production model
            os.makedirs(self.model_evaluation_config.GCS_MODEL_DIR_PATH, exist_ok=True)
            
            """
            Parameters : 
            (a) gcp_bucket_name: bucket name in the GCS (Google CLoud Storage)
            (b) gcs_filename: name of the file present in the above gcp bucket, gcs_filename should match exactly
            (c) destination_dir: Local directory path or GCS dir path to download the file to
            (d) new_filename : name given to the file being downloaded from GCS
                
            """
            self.gcloud.sync_folder_from_gcloud(gcp_bucket_name=self.model_evaluation_config.BUCKET_NAME,
                                                gcs_filename=self.model_evaluation_config.MODEL_NAME,
                                                destination_dir=self.model_evaluation_config.GCS_MODEL_DIR_PATH,
                                                new_filename=self.model_evaluation_config.MODEL_NAME)
            
           
            gcs_model_path = os.path.join(self.model_evaluation_config.GCS_MODEL_DIR_PATH,
                                           self.model_evaluation_config.MODEL_NAME)
            
            
            logging.info("Exited the get_best_model_from_gcloud method of ModelEvaluation class.")
            
            return gcs_model_path
        
        except Exception as e :
            
            raise CustomException(e, sys) from e
        
        
    def evaluate(self, loaded_model):
        
        """
        returns test accuracy metric
        """
        try :
            
            logging.info("Entered the evaluate method  of ModelEvaluation class inside hate_speech/components/model_evaluation.py")
            
            # For debugging purpose
            #print(self.model_trainer_artifacts.x_test_path)
            
            x_test=pd.read_csv(self.model_trainer_artifacts.x_test_path,
                               index_col=0)
            
            # For Debugging purpose
            #print(x_test.head())
            
            y_test=pd.read_csv(self.model_trainer_artifacts.y_test_path,
                               index_col=0)
            
            # For Debugging purpose
            #print(y_test.head())
            
            
            with open('tokenizer.pickle','rb') as handle:
                
                tokenizer=pickle.load(handle)
                
            
            x_test=x_test['tweet'].astype(str)
            x_test = x_test.squeeze()
            
            y_test = y_test.squeeze()
            
            print(f"x_test shape : {x_test.shape}\n")
            print(f"y_test shape : {y_test.shape}")
            
            test_sequences=tokenizer.texts_to_sequences(x_test)
            test_sequences_matrix=pad_sequences(test_sequences, maxlen=MAX_LEN)
            
            
            print(f"-------------test_sequences_matrix-------------\n",test_sequences_matrix,"\n\n")  
                    
            test_loss, test_accuracy = loaded_model.evaluate(test_sequences_matrix, y_test)
            
            logging.info(f"The test accuracy : {test_accuracy}")
            logging.info(f"The test loss : {test_accuracy}")
            
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
        
        Note : We will push the trained model to the GCS bucket as our Production model iff production 
               model accuracy is less than the trained model accuracy using is_trained_model_accepted bool parameter
        """
        
        logging.info("Initiate Model Evaluation")
        
        try:
            
            logging.info("Loading currently trained model")
            
            trained_model=keras.models.load_model(self.model_trainer_artifacts.trained_model_path)
            
            
            # Calling evaluate method
            trained_model_accuracy=self.evaluate(loaded_model=trained_model)
            print(f"Trained model accuracy : {trained_model_accuracy}")
            
            logging.info("fetching the best/production model from gcloud bucket storage for comparison to trained model")
            gcs_model_path=self.get_best_model_from_gcloud()
            
            
            logging.info("Checking if best/production model is present in the GCS bucket storage or not ?")
              
            # this checks whether production model is present in the gcloud or not.
            if not os.path.isfile(gcs_model_path):
                
                # No model is present in the gcloud bucket storage.
                # Therefore we need to push the current trained model to gloud.
                is_trained_model_accepted = True
                trained_model.save(f"ProductionModel/{MODEL_NAME}")
                
                logging.info("No model is present in the GCS bucket.Therefore need to push the current trained model to GCS bucket.")
            
            else:
                
                logging.info("Loaded the best model fetched from GCS bucket")
                
                gcs_loaded_model= keras.models.load_model(gcs_model_path)
                
                gcs_loaded_model_accuracy = self.evaluate(loaded_model=gcs_loaded_model)
                
                print(f"Already present gcs model accuracy : {gcs_loaded_model_accuracy}")
                
                logging.info("Comparing the accuracy on test data using recently trained model and gcs model.")
                
                if gcs_loaded_model_accuracy > trained_model_accuracy :
                    
                    logging.info("gcs loaded model accuracy is more than trained model accuracy.")
                    
                    print("gcs loaded model accuracy is more than trained model accuracy.")
                    # Therefore, no need to push the recently trained model to GCS bucket as our production model
                    is_trained_model_accepted = False
                    
                    gcs_loaded_model.save(f"ProductionModel/{MODEL_NAME}")
                    
                    logging.info("Trained model not accepted")
                    
                else :
                    
                    logging.info("gcs loaded model accuracy is lower than trained model accuracy.")
                    
                    print("gcs loaded model accuracy is lower than trained model accuracy.")
                    
                    # Therefore, Need to push the recently trained model to GCS bucket as our Production model.
                    is_trained_model_accepted = True 
                    
                    trained_model.save(f"ProductionModel/{MODEL_NAME}")
                    
                    print("Trained model accepted for GCS push...")
                    logging.info("Trained model accepted for GCS push...")
             
                    
            model_evaluation_artifacts = ModelEvaluationArtifacts(is_trained_model_accepted=is_trained_model_accepted)
            
            logging.info("Returning the ModelEvaluationArtifacts")
                    
            return model_evaluation_artifacts
        
        except Exception as e :
            
            raise CustomException(e, sys) from e
                
            
            
            
        
        
        
