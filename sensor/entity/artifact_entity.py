from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str
@dataclass
class DataValidationArtifacts:
    report_file_path:str
class DataTransformationArtifacts:...
class ModelTrainingArtifacts:...
class ModelEvaluationArtifacts:...
class ModelPusherArtifacts:...