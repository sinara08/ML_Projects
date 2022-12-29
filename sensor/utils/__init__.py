import pandas as pd
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException
import sys

def get_collection_as_dataframe(database_name, collection_name):
    try:
        logging.info('Reading data from database:{0} and collection {1}'.format(database_name, collection_name))
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info('Found columns: {}'.format(df.columns))
        if '_id' in df.columns:
            df = df.drop('_id', axis=1)

        logging.info('Rows and columns in df = {}'.format(df.shape))
        return df
    except Exception as e:
        logging.debug('Stopping the test_logger_and_exception')
        raise SensorException(e, sys)
