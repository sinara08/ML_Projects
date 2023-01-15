import os, sys
from datetime import datetime
from sensor.logger import logging
from sensor.exception import SensorException

FILE_NAME = 'sensor.csv'
TRAIN_FILE_NAME = 'train.csv'
TEST_FILE_NAME = 'test.csv'
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = 'model.pkl'


class TrainingPipelineConfig:
    def __init__(self):
        self.artifact_dir: str = os.path.join(os.getcwd(),'artifact', datetime.now().strftime("%m_%d_%Y_%H_%M_%S"))

class DataIngestionConfig:
    def __init__(self, training_pipeline_config ):
        self.database_name = 'aps'
        self.collection_name = 'sensor'

        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir, 'data_ingestion')

        self.feature_store_file_path = os.path.join(
             self.data_ingestion_dir, 'feature_store',FILE_NAME)

        self.training_file_path = os.path.join(
             self.data_ingestion_dir, 'dataset', TRAIN_FILE_NAME)

        self.testing_file_path = os.path.join(
             self.data_ingestion_dir, 'dataset', TEST_FILE_NAME)

        self.test_size = 0.2
        # self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        # self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME

    def to_dict(self):
        try:
            return self.__dict__

        except Exception as e:
            raise SensorException(e, sys)

class DataValidationConfig:
    def __init__(self, training_pipeline_config):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, 'data_validation')
        self.report_file_path = os.path.join(self.data_validation_dir, 'report.yaml')
        self.threshold_missing_values = 0.2
        self.base_file_path = os.path.join('aps_failure_training_set1.csv')
class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,
                                                         'data_transformation')
        self.transformed_train_file_path = os.path.join(self.data_transformation_dir,
                                                             "transformer",
                                                             TRAIN_FILE_NAME.replace("csv", "npz") )
        self.transformed_test_file_path = os.path.join(self.data_transformation_dir,
                                                            "transformer",
                                                            TEST_FILE_NAME.replace("csv", "npz") )
        self.transformed_object_file_path = os.path.join(self.data_transformation_dir,
                                                              "transformer",
                                                              TRANSFORMER_OBJECT_FILE_NAME )
        self.target_encoder_path = os.path.join(self.data_transformation_dir,
                                                              "target_encoder",
                                                              TARGET_ENCODER_OBJECT_FILE_NAME )
class ModelTrainingConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_trainer_dir = os.path.join(
            training_pipeline_config.artifact_dir, "model_trainer"
        )
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir, "trained_model", MODEL_FILE_NAME
        )
        self.expected_accuracy = 0.7
        self.overfitting_underfitting_threshold = 0.1
class ModelEvaluationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.change_threshold  = 0.01
class ModelPusherConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir , "model_pusher")
        self.saved_model_dir = os.path.join("saved_models")
        self.pusher_model_dir = os.path.join(self.model_pusher_dir,"saved_models")
        self.pusher_model_path = os.path.join(self.pusher_model_dir,MODEL_FILE_NAME)
        self.pusher_transformer_path = os.path.join(self.pusher_model_dir,TRANSFORMER_OBJECT_FILE_NAME)
        self.pusher_target_encoder_path = os.path.join(self.pusher_model_dir,TARGET_ENCODER_OBJECT_FILE_NAME)