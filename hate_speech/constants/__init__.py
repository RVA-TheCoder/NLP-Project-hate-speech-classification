import os
from datetime import datetime
from pathlib import Path

# Common Constants
TIMESTAMP : str = datetime.now().strftime("%b_%d_%Y_%H_%M_%S")
ARTIFACTS_DIR = Path(os.path.join("artifacts", TIMESTAMP))
BUCKET_NAME='hate-speech-project01'

ZIP_FILENAME='dataset.zip'
LABEL="label"
TWEET="tweet"


# Data-Ingestion Constants
DATA_INGESTION_ARTIFACT_DIR="DataIngestionArtifacts"
DATA_INGESTION_IMBALANCE_DATA_DIR="imbalanced_data.csv"
DATA_INGESTION_RAW_DATA_DIR="raw_data.csv"


# Data transformation constants (DataTransformationconfig)
DATA_TRANSFORMATION_ARTIFACTS_DIR='DataTransformationArtifacts'
TRANSFORMED_FILENAME='final.csv'
DATA_DIR='data'
ID='id'
AXIS=1
INPLACE=True
DROP_COLUMNS=['count', 'hate_speech', 'offensive_language', 'neither']
CLASS='class'

















