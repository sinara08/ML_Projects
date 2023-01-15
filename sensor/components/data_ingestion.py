from sensor import utils
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
import pandas as pd
from sklearn.model_selection import train_test_split
#from pandas import DataFrame
import numpy as np

class DataIngestion:
    def __init__(self, data_ingestion_config):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_ingestion(self) :
        try:
            logging.info('Exporting df as collection of df')
            #Exporting df as collection of df
            df = utils.get_collection_as_dataframe(database_name = self.data_ingestion_config.database_name,
                                                   collection_name = self.data_ingestion_config.collection_name)
            #save data in feature_store
            logging.info('save data in feature_store')
            df.replace(to_replace = "na", value = np.NAN, inplace = True)

            #create feature store folder if not available
            logging.info('create feature store folder if not available')
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok = True)

            #Save df to feature store folder
            logging.info('Save df to feature store folder')
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path, index=False, header= True)

            #split dataset into train and test set
            logging.info('split dataset into train and test set')
            train_df, test_df = train_test_split(df, test_size = self.data_ingestion_config.test_size, random_state = 42 )

            # create dataset folder if not available
            logging.info('create dataset folder if not available')
            dataset_dir = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dataset_dir, exist_ok=True)

            # Save df to feature store folder
            logging.info('Save df to feature store folder')
            train_df.to_csv(path_or_buf=self.data_ingestion_config.training_file_path, index=False, header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.testing_file_path, index=False, header=True)

            data_ingestion_artifact = artifact_entity.DataIngestionArtifacts(feature_store_file_path = self.data_ingestion_config.feature_store_file_path,
                                                   train_file_path = self.data_ingestion_config.training_file_path,
                                                   test_file_path = self.data_ingestion_config.testing_file_path)

            #dataframe = self.export_data_into_feature_store()
            #dataframe = dataframe.drop(self._schema_config["drop_columns"], axis=1)
            #self.split_data_as_train_test(dataframe=dataframe)
            logging.info('data_ingestion_artifact is completed')
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)