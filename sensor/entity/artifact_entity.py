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

@dataclass
class ModelTrainingArtifacts:
    model_path:str
    f1_train_score:float
    f1_test_score:float

@dataclass
class ModelEvaluationArtifacts:
    is_model_accepted: bool
    improved_accuracy: float

@dataclass
class ModelPusherArtifacts:
    pusher_model_dir:str
    saved_model_dir:str