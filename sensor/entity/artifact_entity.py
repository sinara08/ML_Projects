from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifacts:
    report_file_path:str

@dataclass
class DataTransformationArtifacts:
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str
    target_encoder_path:str

class ModelTrainingArtifacts:...
class ModelEvaluationArtifacts:...
class ModelPusherArtifacts:...