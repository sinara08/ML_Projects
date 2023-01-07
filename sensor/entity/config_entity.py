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
                                                             "train.csv" )
        self.transformed_test_file_path = os.path.join(self.data_transformation_dir,
                                                            "transformer",
                                                            "test.csv" )
        self.transformed_object_file_path = os.path.join(self.data_transformation_dir,
                                                              "transformer",
                                                              TRANSFORMER_OBJECT_FILE_NAME )
        self.target_encoder_path = os.path.join(self.data_transformation_dir,
                                                              "target_encoder",
                                                              TARGET_ENCODER_OBJECT_FILE_NAME )
class ModelTrainingConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...