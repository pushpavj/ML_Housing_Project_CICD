from housing.entity.config_entity import DataIngestionConfig, DataValidationConfig, \
    ModelTrainerConfig, DataTransofrmationConfig, ModelEvaluationConfig, ModelPusherConfig,\
        TrainingPipelineConfig

from housing.util.util import read_yaml_file

from constant import * # it gives all the constant declared inside the constant file

import os, sys

from housing.exception import HousingException
from housing.logger import logging

ROOT_DIR=os.getcwd() # to get current working directory


class Configuration: 

    def __init__ (self,config_file_path =CONFIG_FILE_PATH,
                  current_time_stamp:str= CURRENT_TIME_STAMP)-> None:
        print("CONFIG FILE PATH2 =", CONFIG_FILE_PATH)
        print("config_file_path =", config_file_path)
        try:
            self.config_info=read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config=self.get_trianing_pipeline_config()
            self.time_stamp=current_time_stamp
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            data_ingestion_info=self.config_info[DATA_INGESTION_CONFIG_KEY]

            artifact_dir=self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir=os.path.join (
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
                 )
            dataset_download_url=data_ingestion_info[DATASET_DOWNLOAD_URL_KEY]
            raw_data_dir=os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[RAW_DATA_DIR_KEY]
                )
            tgz_download_dir=os.path.join(
            data_ingestion_artifact_dir,
            data_ingestion_info[TGZ_DOWNLOAD_DIR_KEY]
                )
            ingested_dir=os.path.join(
            data_ingestion_artifact_dir,
            data_ingestion_info[INGESTED_DIR_KEY])

            ingested_train_dir=os.path.join(
                ingested_dir,
                data_ingestion_info[INGESTED_TRAIN_DIR_KEY]
                )
            ingested_test_dir=os.path.join(
                ingested_dir,
                data_ingestion_info[INGESTED_TEST_DIR_KEY]
                )

            data_ingestion_config=DataIngestionConfig(
            dataset_download_url=dataset_download_url,
            tgz_download_dir=tgz_download_dir,
            raw_data_dir=raw_data_dir,
            ingested_train_dir=ingested_train_dir,
            ingested_test_dir=ingested_test_dir)

            return data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_validation_config(self)->DataValidationConfig:
        pass

    def get_data_transformation_config(self)->DataTransofrmationConfig:
        pass

    def get_model_trainer_config(self)->ModelTrainerConfig:
        pass

    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        pass
    
    def get_model_pusher_config(self)->ModelPusherConfig:
        pass

    def get_trianing_pipeline_config(self)->TrainingPipelineConfig:
        
        try:
            training_pipeline_config=self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir=os.path.join(ROOT_DIR, training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            #this gives the path of the artifact folder
            #'d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact'
            #Check example.ipbynb for more details on how does this code works
            training_pipeline_config=TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f'TrainingPieplineConfig: {training_pipeline_config}')
            return training_pipeline_config




        except Exception as e:
            raise HousingException(e,sys) from e
     