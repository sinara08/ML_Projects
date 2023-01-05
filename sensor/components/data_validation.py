
from sensor.entity import artifact_entity, config_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
from typing import Optional
from sensor import utils

class DataValidation:
    def __init__(self, data_validation_config, data_ingesion_artifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.validation_error = dict()
            self.data_ingesion_artifact = data_ingesion_artifact
            #self.base_
        except Exception as e:
            raise SensorException(e, sys)

    def drop_cols_missing_values(self, df, report_key_name):
        """
        This function drop columns which has missing value above the given threshold value
        :param df:
        :param threshold:
        :return: Option[df] - if
        """
        try:
            threshold = self.data_validation_config.threshold_missing_values
            null_rpt = df.isna().sum()/df.shape[0]
            #selecting column names which has missing values
            logging.info('selecting column names which has missing values')
            logging.info(null_rpt)
            drop_cols = null_rpt[null_rpt > threshold].index
            logging.info(drop_cols)
            self.validation_error[report_key_name] = list(drop_cols)

            df.drop(list(drop_cols),axis=1, inplace=True)
            if len(df.columns) == 0:
                logging.info('Returned None')
                return None

            logging.info('len of columns is not 0')
            return df
        except Exception as e:
            SensorException(e, sys)

    def is_required_cols_exist(self, base_df, present_df, report_key_name):
        try:
            logging.info('In is_required_cols_exist')
            base_cols = base_df.columns
            present_cols = present_df.columns

            logging.info('Retrieving Missing columns')
            missing_cols = []
            for base_col in base_cols:
                if base_col not in present_cols:
                    logging.info(f"Column: [{base_col} is not available]")
                    missing_cols.append(base_col)
            #[missing_cols.append(base_col) for base_col in base_cols if base_col not in present_cols]

            if len(missing_cols) > 0:
                self.validation_error[report_key_name] = missing_cols
                return False

            return True
        except Exception as e:
            raise SensorException(e, sys)

    def data_drift(self,base_df, present_df, report_key_name):
        try:
            drift_rpt = dict()
            base_cols = base_df.columns
            present_cols = present_df.columns

            logging.info(f'Checking if data drift is existing {report_key_name}')
            for base_col in base_cols:
                base_data, curr_data = base_df[base_col], present_df[base_col]
                same_dist = ks_2samp(base_data, curr_data)

                logging.info(f'p Value {same_dist.pvalue}')
                if same_dist.pvalue > 0.05:
                    #Accept Null Hypothesis
                    #both cols are from same distribution
                    drift_rpt[base_col] = {
                        "Pvalue":float(same_dist.pvalue),
                        "Same Distribution": True,
                        "Column Name": base_col,
                        "report_key_name": report_key_name
                    }
                else:
                    # different distribution
                    drift_rpt[base_col] = {
                        "Pvalue": float(same_dist.pvalue),
                        "Same Distribution": False,
                        "Column Name": base_col,
                        "report_key_name": report_key_name
                    }
            self.validation_error[report_key_name] = drift_rpt
        except Exception as e:
            SensorException(e, sys)

    def initiate_data_validation(self):
        try:
            logging.info('Initiate Data Validation')
            logging.info(self.data_validation_config.base_file_path)
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NAN},inplace=True)
            logging.info('Replacing na with np.NAN')
            base_df = self.drop_cols_missing_values(base_df, report_key_name = "missing_data_in_base_data_set")
            logging.info('Dropping columns with NULL values from base_df')
            logging.info(base_df)

            logging.info('Reading train data frame')
            train_df = pd.read_csv(self.data_ingesion_artifact.train_file_path)
            logging.info('Dropping columns with NULL values from train_df')
            train_df = self.drop_cols_missing_values(train_df, report_key_name = "missing_data_in_train_data_set")


            logging.info('Reading test data frame')
            test_df = pd.read_csv(self.data_ingesion_artifact.test_file_path)
            logging.info('Dropping columns with NULL values from test_df')
            test_df = self.drop_cols_missing_values(test_df, report_key_name = "missing_data_in_test_data_set")

            exclude_cols = ['class']
            base_df = utils.convert_columns_float(base_df, exclude_cols)
            train_df = utils.convert_columns_float(train_df, exclude_cols)
            test_df = utils.convert_columns_float(test_df, exclude_cols)

            logging.info('Is all required columns present in train df')
            train_cols_status = self.is_required_cols_exist(base_df, train_df,
                                                            report_key_name="required_cols_in_train_data_set")
            if train_cols_status:
                self.data_drift(base_df, train_df, report_key_name="data_drift_in_train_data_set")

            logging.info('Is all required columns present in test df')
            test_cols_status = self.is_required_cols_exist(base_df, test_df, report_key_name = "required_cols_in_test_data_set")
            if test_cols_status:
                self.data_drift(base_df, test_df,report_key_name = "data_drift_in_test_data_set")

            utils.write_yaml_file(self.data_validation_config.report_file_path, self.validation_error)
            data_validation_artifact = artifact_entity.DataValidationArtifacts(self.data_validation_config.report_file_path)
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)

