from dataclasses import dataclass

# Data Ingestion artifacts
@dataclass
class DataIngestionArtifacts:
    
    imbalance_data_filepath:str
    raw_data_filepath:str
    
    
    
# Data Transformation artifacts
@dataclass
class DataTransformationArtifacts:
    
    transformed_data_filepath:str
    
    
# Model Trainer Artifact
@dataclass
class ModelTrainerArtifacts:
    
    
    trained_model_path:str
    x_test_path:list
    y_test_path:list
    

# Model Evaluation Artifact
@dataclass
class ModelEvaluationArtifacts:
    
    """
    We will push the trained model to the gcloud as our Production model iff best/production 
    model accuracy (already present in the gcloud) is less than the trained model accuracy 
    using is_trained_model_accepted bool parameter.
    
    """
    
    is_trained_model_accepted:bool
    

@dataclass
class ModelPusherArtifacts:
    
    bucket_name:str
    
        
  
    
    
    
    