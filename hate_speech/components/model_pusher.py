import sys
from hate_speech.logger import logging
from hate_speech.exception import CustomException

from hate_speech.configuration.gcloud_syncer import GCloudSync
from hate_speech.entity.config_entity import ModelPusherConfig
from hate_speech.entity.artifact_entity import ModelPusherArtifacts





class ModelPusher:
    
    def __init__(self, model_pusher_config:ModelPusherConfig):
        
        self.model_pusher_config=model_pusher_config
        self.gcloud=GCloudSync()
        
    
    def initiate_model_pusher(self) ->ModelPusherArtifacts:
        
        """
        Returns : Model pusher artifact after initiating the model pusher
        """
        
        logging.info("Entered initiate_model_pusher method of ModelPusher class inside hate_speech/components/model_pusher.py")
        
        try:
            
            """
                Parameters : 
                (a) gcp_bucket_name: bucket name in the GCS (Google CLoud Storage)
                (b) source_dir : source directory path from where we want to copy item(s)
                (c) source_filename : source filename (present inside source_dir) that we want to copy.
               
            """
            
            
            # Uploading the model to gcloud storage
            self.gcloud.sync_folder_to_gcloud(
                source_dir="ProductionModel",
                source_filename=self.model_pusher_config.MODEL_NAME,
                gcp_bucket_name=self.model_pusher_config.BUCKET_NAME,
                )
                 
            logging.info("Uploaded the Production model to gcloud storage.")
            
            # Saving the model pusher artifacts
            model_pusher_artifact = ModelPusherArtifacts(bucket_name=self.model_pusher_config.BUCKET_NAME)
            
            logging.info("Exited the initiate_model_pusher method of ModelPusher class")
            
            return model_pusher_artifact
    

        except Exception as e:
            raise CustomException(e,sys) from e
        
        






