from sensor.logger import logging
from sensor.exception import SensorException
import sys
from sensor.entity import config_entity


def test_logger_and_exception():
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config)
        print(data_ingestion_config.to_dict())
    except Exception as e:
        logging.debug('Stopping the test_logger_and_exception')
        raise SensorException(e, sys)

if __name__ == '__main__':
    try:
        test_logger_and_exception()
    except Exception as e:
        raise SensorException(e, sys)