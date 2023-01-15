from sensor.pipeline.training_pipeline import  start_training_pipeline
from sensor.exception import SensorException
from sensor.pipeline.batch_prediction import start_batch_prediction

file_path="/Users/nikhilgopalakrishnan/PycharmProjects/sensor-fault-detection/aps_failure_training_set1.csv"

import os, sys

print(__name__)

if __name__ == '__main__':
    try:
        #start_training_pipeline()
        output_file = start_batch_prediction(input_file_path=file_path)
        print(output_file)
    except Exception as e:
        raise SensorException(e, sys)