from sensor.entity import artifact_entity, config_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sensor import utils
from sklearn.metrics import f1_score

class ModelTrainer:
    def __init__(self, model_trainer_config, data_transformation_artifact):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise SensorException(e, sys)

    def fine_tune(self, x, y):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)

    def train_model(self, x, y):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_trainer(self):
        try:
            logging.info('Loading training and testing array')
            train_arr = utils.load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = utils.load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)

            logging.info('Splitting input and target feature from both train and test array')
            x_train, y_train = train_arr[:,:-1], train_arr[:,-1]
            x_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            logging.info('Train the model')
            model = self.train_model(x_train, y_train)

            logging.info('Calculate Train score')
            yhat_train = model.predict(x_train)

            f1_train_score = f1_score(y_true = y_train, y_pred = yhat_train)

            logging.info('Calculate Test score')
            yhat_test = model.predict(x_test)

            f1_test_score = f1_score(y_true=y_test, y_pred=yhat_test)

            logging.info(f'f1_train_score: {f1_train_score} and f1_test_score:{f1_test_score}')
            logging.info('Checking if model is underfit or not')
            #Check for overfitting or underfitting or expected score
            if f1_test_score < self.model_trainer_config.expected_accuracy:
                raise Exception(f'Model is not good as it is not able to give expected accuracy {self.model_trainer_config.expected_accuracy} and actual accuracy {f1_test_score}')

            logging.info('Checking if model is overfit or not')
            diff = abs(f1_train_score-f1_test_score)

            if diff > self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception(f'Train and Test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_underfitting_threshold}')

            #Save the trained model
            logging.info('Save the model')
            utils.save_object(file_path = self.model_trainer_config.trained_model_file_path, obj = model)

            #Prepare artifact
            logging.info('Prepare  the artifact')
            model_trainer_artifact = artifact_entity.ModelTrainingArtifacts(self.model_trainer_config.trained_model_file_path, f1_train_score, f1_test_score)
            logging.info(f'Model trainer Artifact : {model_trainer_artifact}')
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)
