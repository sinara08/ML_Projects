from sensor import utils
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
class DataIngestion:
    def __init__(self, data_ingestion_config):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feature_store()
            dataframe = dataframe.drop(self._schema_config["drop_columns"], axis=1)
            self.split_data_as_train_test(dataframe=dataframe)

            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)