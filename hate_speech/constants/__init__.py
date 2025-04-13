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


# Model training constants
MODEL_TRAINER_ARTIFACTS_DIR ='ModelTrainerArtifacts'
TRAINED_MODEL_DIR='trained_model'
TRAINED_MODEL_NAME='trained_model.keras'

X_TEST_FILENAME='x_test.csv'
Y_TEST_FILENAME='y_test.csv'

X_TRAIN_FILENAME='x_train.csv'

RANDOM_STATE=42
EPOCH=1
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
BEST_MODEL_DIR='best_model'
MODEL_EVALUATION_FILENAME='loss.csv'

MODEL_NAME='trained_model.keras'
APP_HOST="0.0.0.0"
APP_PORT=8080





