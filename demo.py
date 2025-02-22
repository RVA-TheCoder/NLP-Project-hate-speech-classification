from hate_speech.logger import logging
from hate_speech.exception import CustomException
import sys
from hate_speech.configuration.gcloud_syncer import GCloudSync



#logging.info("Welcome to the my project Hate speech classification.")

# try :

#     a = 7/'2'

# except Exception as e :

#     raise CustomException(e, sys) from e


gcloud_obj=GCloudSync()
# downloading the file from the gcp bucket
gcloud_obj.sync_folder_from_gcloud(gcp_bucket_url="hate-speech-project01", 
                                   filename="dataset.zip",
                                   destination="data/dataset.zip")








