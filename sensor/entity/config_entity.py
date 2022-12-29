import os, sys
from datetime import datetime
from sensor.logger import logging
from sensor.exception import SensorException

FILE_NAME = 'sensor.csv'
TRAIN_FILE_NAME = 'train.csv'
TEST_FILE_NAME = 'test.csv'


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

        # self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        # self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME

    def to_dict(self):
        try:
            return self.__dict__

        except Exception as e:
            raise SensorException(e, sys)

class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainingConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...