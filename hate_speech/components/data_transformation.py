import os, re, sys, string
import pandas as pd
from sklearn.model_selection import train_test_split

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')


from hate_speech.logger import logging
from hate_speech.exception import CustomException

from hate_speech.entity.config_entity import DataTransformationConfig
from hate_speech.entity.artifact_entity import (DataIngestionArtifacts, 
                                                DataTransformationArtifacts)


class DataTransformation:
    
    def __init__(self, data_transformation_config:DataTransformationConfig,
                 data_ingestion_artifacts:DataIngestionArtifacts ):
        
        self.data_transformation_config=data_transformation_config
        self.data_ingestion_artifacts=data_ingestion_artifacts
        
        
    def imbalance_data_cleaning(self):
        
        try:
            
            logging.info("Entered into the imbalance_data_cleaning method of class DataTransformation inside hate_speech/components/data_transformation.py")
            
            imbalance_data=pd.read_csv(filepath_or_buffer=self.data_ingestion_artifacts.imbalance_data_filepath)
            
            # Dropping the 'ID' column inside imbalanced_data.csv file because it's not needed
            imbalance_data.drop(self.data_transformation_config.ID,
                                axis=self.data_transformation_config.AXIS,
                                inplace=self.data_transformation_config.INPLACE)
            
            logging.info(f"Exited the imbalance_data_cleaning method and returned imbalance data {imbalance_data}")
        
            return imbalance_data
        
        except Exception as e:
            
            raise CustomException(e,sys) from e
        
    
    def raw_data_cleaning(self):
        
        try :
            
            logging.info("Entered into the raw_data_cleaning function of class DataTransformation inside hate_speech/components/data_transformation.py")
        
            raw_data=pd.read_csv(filepath_or_buffer=self.data_ingestion_artifacts.raw_data_filepath,
                                 index_col=0)
            
            # Dropping unnecessary columns
            raw_data.drop(self.data_transformation_config.DROP_COLUMNS,
                          axis=self.data_transformation_config.AXIS,
                          inplace=self.data_transformation_config.INPLACE)
            
            # Replacing class=0 to class=1 in raw_data.csv file
            raw_data[raw_data[self.data_transformation_config.CLASS]==0][self.data_transformation_config.CLASS]=1
            
            # replacing class=0 to class=1 in raw_data.csv file
            raw_data[self.data_transformation_config.CLASS].replace({0:1},inplace=True)

            #  replacing class=2 to class=0 in raw_data.csv file
            raw_data[self.data_transformation_config.CLASS].replace({2:0}, inplace = True)

            # rename the column 'class' to 'label' in raw_data.csv' file
            raw_data.rename(columns={self.data_transformation_config.CLASS:self.data_transformation_config.LABEL},inplace =True)
            
            logging.info(f"Exited the raw_data_cleaning function and returned the raw_data {raw_data}")
            
            return raw_data

        except Exception as e:
            raise CustomException(e,sys) from e
        
        
    def concat_dataframe(self,dfs):
        
        """
            dfs : list of pandas DFs to be concatenated.
        """
        try:
            
            logging.info("Entered into the concat_dataframe method of class DataTransformation inside hate_speech/components/data_transformation.py")
            
            # Lets concatenate both raw and imbalance data.csv file after cleaning
            df=pd.concat(dfs)
            
            # For debugging purpose
            print("Concatenated DataFrame : ",df.head(),"\n\n") 
            
            logging.info(f"returned the concatenated dataframe {df}")
            
            return df
        
        except Exception as e:
            
            raise CustomException(e,sys) from e
        
    
    def concat_df_text_preprocessing(self,words):
        
        try:
            
            logging.info("Entered into the concat_df_text_preprocessing method of class DataTransformation inside hate_speech/components/data_transformation.py")
            
            # Lets apply the text preprocessing on the concatenated dfs
            stemmer = nltk.SnowballStemmer("english")
            stopword = set(stopwords.words('english'))
            
            words = str(words).lower()
            words = re.sub('\[.*?\]', '', words)
            words = re.sub('https?://\S+|www\.\S+', '', words)
            words = re.sub('<.*?>+', '', words)
            words = re.sub('[%s]' % re.escape(string.punctuation), '', words)
            words = re.sub('\n', '', words)
            words = re.sub('\w*\d\w*', '', words)
            
            # Stopword removal
            #words = [word for word in words.split(' ') if words not in stopword]
            #words=" ".join(words)
            
            # stemming
            #words = [stemmer.stem(word) for word in words.split(' ')]
            #words=" ".join(words)
            
            logging.info("Exited the concat_data_cleaning function")
            
            # Returned a cleaned text string
            return words 

        except Exception as e:
            raise CustomException(e, sys) from e
        
        
    def initiate_data_transformation(self) ->DataTransformationArtifacts:
        
        try :
            
            logging.info("Entered the initiate_data_transformation method of class DataTransformation inside hate_speech/components/data_transformation.py")
            
            # calling method to get cleaned imbalance data in .csv format
            imbalanced_data_cleaned=self.imbalance_data_cleaning()
            # calling method to get cleaned raw data in .csv format
            raw_data_cleaned=self.raw_data_cleaning()
            
            # Concatenating the above two .csv files
            dfs=[imbalanced_data_cleaned,raw_data_cleaned] 
            df=self.concat_dataframe(dfs=dfs)
            
            # Applying text preprocessing method on the class tweet of the concatenated dfs
            df[self.data_transformation_config.TWEET]= df[self.data_transformation_config.TWEET].apply(self.concat_df_text_preprocessing)
                                                                                                        
            # Saving the file to the DataTransformationArtifact directory                                                                                      )
            os.makedirs(self.data_transformation_config.DATA_TRANSFORMATION_ARTIFACTS_DIR,
                        exist_ok=True)
            
            df.to_csv(self.data_transformation_config.TRANSFORMED_DATA_FILEPATH, index=False, header=True)
            
            # creating object of DataTransformationArtifacts class
            data_transformation_artifact=DataTransformationArtifacts(
                                         transformed_data_filepath=self.data_transformation_config.TRANSFORMED_DATA_FILEPATH
                                         )
            
            logging.info("Returning the DataTransformationArtifacts")
            
            return data_transformation_artifact
        
        except Exception as e:
            raise CustomException(e,sys) from e
        
        
    
        
        
            
            
        