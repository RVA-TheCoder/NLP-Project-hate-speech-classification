import os, sys, pickle
import pandas as pd

from hate_speech.logger import logging
from hate_speech.exception import CustomException
from hate_speech.constants import *

from sklearn.model_selection import train_test_split

from tensorflow.keras.preprocessing.text import Tokenizer

from keras.utils import pad_sequences

from hate_speech.entity.config_entity import ModelTrainerConfig
from hate_speech.entity.artifact_entity import (ModelTrainerArtifacts, DataTransformationArtifacts)

from hate_speech.ml.model import ModelArchitecture




class ModelTrainer:
    
    def __init__(self, data_transformation_artifacts:DataTransformationArtifacts,
                 model_trainer_config:ModelTrainerConfig ):
        
        self.data_transformation_artifacts = data_transformation_artifacts
        self.model_trainer_config=model_trainer_config
        
        
    
    def splitting_data(self, csv_path):
        
        """
        csv_path:str: complete concatenated pandas DF path
        
        returns : (x_train, y_train, x_test, y_test) tuple
        """
        try: 
            
            logging.info("Entered the splitting_data method of class ModelTrainer inside hate_speech/components/model_trainer.py")
            logging.info("Reading the data")
            
            
            df = pd.read_csv(csv_path, index_col=False)
            
            # Boolean mask for string type values inside df[TWEET] column
            print("Number of rows in final_df before : ",len(df))
            boolean_result = df[TWEET].apply(lambda x: isinstance(x, str))
            df = df[boolean_result]
            print("Number of rows in final_df After : ",len(df),"\n\n")
            
            logging.info("Splitting the data into x and y")
            
            # Separating the independent and dependent variable
            x=df[TWEET] # independent variable
            y=df[LABEL] # dependent variable
            
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=TEST_SIZE,
                                                                random_state=RANDOM_STATE)
            # For Debugging Purpose
            #print(len(x_train),len(y_train) )
            #print(len(x_test),len(y_test) )
            
            #print(type(x_train), type(y_train))
            #print(y_train)
            #print("y_train dtype : ",y_train.dtype,"\n\n\n\n")
            #print(y_test)
            #print("y_test dtype : ", y_test.dtype,"\n\n\n\n")
            
            logging.info("Exited the splitting_data method of class ModelTrainer.")
            
            return x_train, y_train, x_test, y_test
        
        
        except Exception as e:
            
            raise CustomException(e ,sys) from e
        
    
    def tokenizing(self,x_train):
        
        try:
            
            logging.info("Entered the tokenizing method of class ModelTrainer inside hate_speech/components/model_trainer.py")
            logging.info("Applying the tokenization on the data.")
           
            # Initiating the object of Tokenizer class
            tokenizer = Tokenizer(num_words=self.model_trainer_config.MAX_WORDS)
            # Fitting the tokenizer on the train data
            tokenizer.fit_on_texts(x_train)
            # converting the texts into sequences array
            sequences = tokenizer.texts_to_sequences(x_train)
            
            logging.info(f"converting text to sequences: {sequences}")
            
            sequences_matrix = pad_sequences(sequences, maxlen=self.model_trainer_config.MAX_LEN)
            logging.info(f" The sequence matrix is: {sequences_matrix}" )
            
            return sequences_matrix, tokenizer
        
        except Exception as e:
            raise CustomException(e, sys) from e
        
        
    def initiate_model_trainer(self,) -> ModelTrainerArtifacts:

        """
        Method Name :   initiate_model_trainer
        Description :   This function initiates a model trainer steps
        
        Output      :   Returns model trainer artifact
        On Failure  :   Write an exception log and then raise an exception
        """

        try:
            
            logging.info("Entered initiate_model_trainer method of class ModelTrainer inside hate_speech/components/model_trainer.py")
            
            # Calling the method
            x_train, y_train, x_test, y_test = self.splitting_data(csv_path=self.data_transformation_artifacts.transformed_data_filepath)
            
            logging.info(f"Xtrain size is : {x_train.shape}")
            logging.info(f"Ytrain size is : {y_train.shape}")
            logging.info(f"Xtest size is : {x_test.shape}")
            logging.info(f"Ytest size is : {y_test.shape}")
            
            # Creating the object of ModelArchitecture class
            model_architecture = ModelArchitecture()   
            model = model_architecture.get_model()

            # Calling the method 
            sequences_matrix,tokenizer =self.tokenizing(x_train)

            # For debugging purpose
            #print(sequences_matrix)
            #print(sequences_matrix.dtype,"\n\n\n\n")
            #print(y_train)
            #print(y_train.dtype,"\n\n\n\n")
            
            logging.info("Entered into model training")
            model.fit(sequences_matrix,
                      y_train, 
                      batch_size=self.model_trainer_config.BATCH_SIZE, 
                      epochs = self.model_trainer_config.EPOCH, 
                      validation_split=self.model_trainer_config.VALIDATION_SPLIT, 
                     )
            
            logging.info("Model training finished")

            # Saving the Tokenizer
            with open('tokenizer.pickle', 'wb') as handle:
                pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
            # Saving the Trained model
            os.makedirs(self.model_trainer_config.TRAINED_MODEL_DIR,exist_ok=True)
            logging.info("saving the model")
            model.save(self.model_trainer_config.TRAINED_MODEL_PATH)
            
            # Saving the data (test and train) for the Model evaluation stage
            x_train.to_csv(self.model_trainer_config.X_TRAIN_DATA_PATH) # incase if required in the later stage
            
            x_test.to_csv(self.model_trainer_config.X_TEST_DATA_PATH)
            y_test.to_csv(self.model_trainer_config.Y_TEST_DATA_PATH)

            
            model_trainer_artifacts = ModelTrainerArtifacts(
                trained_model_path = self.model_trainer_config.TRAINED_MODEL_PATH,
                x_test_path = self.model_trainer_config.X_TEST_DATA_PATH,
                y_test_path = self.model_trainer_config.Y_TEST_DATA_PATH)
            
            logging.info("Returning the ModelTrainerArtifacts")
            
            return model_trainer_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e
        
        
        
        
        
            
                       