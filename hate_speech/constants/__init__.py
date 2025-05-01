import os
from datetime import datetime
from pathlib import Path

# Common Constants

# We can create the ARTIFACTS_DIR based on the TIMESTAMP , below is the code
# TIMESTAMP : str = datetime.now().strftime("%b_%d_%Y_%H_%M_%S")
# root directory for the model artifacts.
# ARTIFACTS_DIR = Path(os.path.join("artifacts", TIMESTAMP))

# ARTIFACTS_DIR without TIMESTAMP , for simplicity purpose
# root directory for the model artifacts.
ARTIFACTS_DIR = Path("artifacts")

# GCP Bucket details
BUCKET_NAME='hate-speech-project01'
GCP_BUCKET_FILENAME='dataset.zip'   # Name of the data file inside gcloud bucket that we'll download


# Data-Ingestion Constants
DATA_INGESTION_ARTIFACT_DIR="DataIngestionArtifacts"
DATA_INGESTION_IMBALANCE_DATA_FILENAME="imbalanced_data.csv"
DATA_INGESTION_RAW_DATA_FILENAME="raw_data.csv"


# Data transformation constants (DataTransformationconfig)
DATA_TRANSFORMATION_ARTIFACTS_DIR='DataTransformationArtifacts'
TRANSFORMED_DATA_FILENAME='data_transformed.csv'

# transformed data ('data_transformed.csv') has two columns: X=Tweet & Y=LABEL
LABEL="label"
TWEET="tweet"

# Below constants are for imbalanced_data.csv
ID='id'
AXIS=1
INPLACE=True

# Below constant 'DROP_COLUMNS' is for raw_data.csv
DROP_COLUMNS=['count', 'hate_speech', 'offensive_language', 'neither']
# Below constant is used to replace class=0 to class=1 in raw_data.csv file
CLASS='class'


# Model training constants
MODEL_TRAINER_ARTIFACTS_DIR ='ModelTrainerArtifacts'
TRAINED_MODEL_DIR='trained_model'
TRAINED_MODEL_NAME='trained_model.keras'

# for skelearn train-test split
TEST_SIZE=0.3
X_TRAIN_FILENAME='x_train.csv'
X_TEST_FILENAME='x_test.csv'
Y_TEST_FILENAME='y_test.csv'



# Model training parameters
RANDOM_STATE=42
EPOCH=2
BATCH_SIZE=128
VALIDATION_SPLIT=0.2


# Model Architecture constants
MAX_WORDS=50000   
MAX_LEN=100
LOSS='binary_crossentropy'
METRICS=['accuracy']
ACTIVATION='sigmoid'


# Model Evaluation constants
MODEL_EVALUATION_ARTIFACTS_DIR='ModelEvaluationArtifacts'
GCS_MODEL_DIR='gcs_model'  # ModelEvaluationArtifacts/gcs_model inside this we'll store GCS production model
MODEL_EVALUATION_FILENAME='model_eval_performance.csv'

# This name is used for best/production model
MODEL_NAME='production_model.keras'

# For RESTAPI
APP_HOST="0.0.0.0"
APP_PORT=8080





