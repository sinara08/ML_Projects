import pandas as pd
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException
import sys, os
import yaml
import dill #to save object in pickle format(serialization)
import numpy as np

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

def write_yaml_file(file_path, data):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir)
        with open(file_path,"w") as fw:
            yaml.dump(data, fw)
    except Exception as e:
        raise SensorException(e, sys)

def convert_columns_float(df, excl_columns):
    try:
        for col in df.columns:
            if col not in excl_columns:
                df[col] = df[col].astype('float')
        return df
    except Exception as e:
        raise SensorException(e, sys)


def save_object(file_path:str, obj):
    try:
        logging.info('Entered save_object method of Utils Class')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj )
        logging.info('Exit the save_object method')

    except Exception as e:
        raise SensorException(e, sys)


def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception('The file {0} does not exist').format(file_path)
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj )
    except Exception as e:
        raise SensorException(e, sys)

def save_numpy_array_data(file_path, array):
    """
    save numpy array data to file
    :param file_path:str location of file to save
    :param array: np.array data to save
    :return:
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok = True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise SensorException(e, sys)

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys)