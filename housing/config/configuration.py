from housing.entity.config_entity import DataIngestionConfig, DataValidationConfig, \
    ModelTrainerConfig, DataTransofrmationConfig, ModelEvaluationConfig, ModelPusherConfig,\
        TrainingPipelineConfig

from housing.util.util import read_yaml_file

from housing.constant import * # it gives all the constant declared inside the constant file

import os, sys

from housing.exception import HousingException
from housing.logger import logging

# This module reads the config.yaml file to get the configuration detail values and 
# make it assigned to config entity strucutre. This also uses the constatn.py to 
# read the config.yaml file. The constant.py has the Constatnt variable name 
# defined for each configuration variable defined under config.yaml. This constant
#.py file is just to make the modularized coding.

ROOT_DIR=os.getcwd() # to get current working directory


class Configuration: 

    def __init__ (self,config_file_path =CONFIG_FILE_PATH,
                  current_time_stamp:str= CURRENT_TIME_STAMP)-> None:
        print("CONFIG FILE PATH2 =", CONFIG_FILE_PATH)
        print("config_file_path =", config_file_path)
        #CONFIG_FILE_PATH is defined under constant which contains the value as path of config.yaml file along with the
        #file name 
        #'ML_Housing_Project_CICD\\config\\config.yaml'
        #CURRENT_TIME_STAMP to get the runtime time stamp
        try:
            self.config_info=read_yaml_file(file_path=config_file_path) #calling the read_yaml_file by passing config.ya
            #mal file path.
            #  Now the self.config_info will have content of config.yaml file as list.
            self.training_pipeline_config=self.get_trianing_pipeline_config()
    #Gets config entity variable training_pipeline_config with artifact_dir sub variable got assigned value as
    #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir
            self.time_stamp=current_time_stamp 
    #Getting the time_stamp value from the constant defined in constant module
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            data_ingestion_info=self.config_info[DATA_INGESTION_CONFIG_KEY]
            #Gets only the Data_ingestion_config group details from the config.yaml file

            artifact_dir=self.training_pipeline_config.artifact_dir
    #artifact_dir gets the value as  
    # #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir
            data_ingestion_artifact_dir=os.path.join (
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,  #Defined in constant module and has value as'data_ingestion'
                self.time_stamp
                 )
    #gives the path as below
    #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS
            dataset_download_url=data_ingestion_info[DATASET_DOWNLOAD_URL_KEY] 
    #Gets the url value as https://raw.githubusercontent.com/ageron/handson-ml/master/dataset/housing/housing.tgz

            raw_data_dir=os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[RAW_DATA_DIR_KEY] #value is raw_data
                )
    #Gets the path as below
    #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\raw_data
            tgz_download_dir=os.path.join(
            data_ingestion_artifact_dir,
            data_ingestion_info[TGZ_DOWNLOAD_DIR_KEY] #value is tgz_data
                )
    #Gets the path as below
    #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\raw_data\\tgz_data
            ingested_dir=os.path.join(
            data_ingestion_artifact_dir,
            data_ingestion_info[INGESTED_DIR_KEY]) # value ingested_data
   #Gets the path as below
    #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\ingested_data
            ingested_train_dir=os.path.join(
                ingested_dir,
                data_ingestion_info[INGESTED_TRAIN_DIR_KEY]#value is train
                )
#Gets the path as below
    #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\ingested_data\\train
            ingested_test_dir=os.path.join(
                ingested_dir,
                data_ingestion_info[INGESTED_TEST_DIR_KEY] #value is test
                )
#Gets the path as below
    #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\ingested_data\\test

#Now settiup the config entity named tuple group variables with the above local
#variables.
            data_ingestion_config=DataIngestionConfig(
            dataset_download_url=dataset_download_url,
            tgz_download_dir=tgz_download_dir,
            raw_data_dir=raw_data_dir,
            ingested_train_dir=ingested_train_dir,
            ingested_test_dir=ingested_test_dir)

            return data_ingestion_config #returning the object of the Dataingesti
            #on config entity with value assigned.
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_validation_config(self)->DataValidationConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir
       #artifact_dir gets the value as  
    # #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir
            data_validation_artifact_dir=os.path.join(artifact_dir,
            DATA_VALIDATION_ARTEFACT_DIR_NAME_KEY,
            self.time_stamp)

            data_validation_config=self.config_info[DATA_VALIDATION_CONFIG_KEY]


            schema_file_path=os.path.join(ROOT_DIR,data_validation_config[DATA_VALIDATION_SCHEMA_DIR_KEY], 
            data_validation_config[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY])

            report_file_path=os.path.join(data_validation_artifact_dir,
            data_validation_config[DATA_VALIDATION_REPORT_FILE_NAME_KEY])

            report_page_file_path=os.path.join(data_validation_artifact_dir,
            data_validation_config[DATA_VALIDATION_REPROT_PAGE_FILE_NAME_KEY])
 
            data_validation_config=DataValidationConfig(schema_file_path=schema_file_path,
            report_file_path=report_file_path, report_page_file_path=report_page_file_path
            )
            return data_validation_config
        except Exception as e:
            raise HousingException(e,sys) from e


    def get_data_transformation_config(self)->DataTransofrmationConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir
       #artifact_dir gets the value as  
    # #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir
            data_trasnformation_artifact_dir=os.path.join(artifact_dir,
            DATA_TRANSFORMATION_ARTIFACT_DIR_KEY,
            self.time_stamp)

            data_transformation_config_info=self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]
            add_bedroom_per_room=data_transformation_config_info[ADD_BEDROOM_PER_ROOM_KEY]

            transformed_train_dir=os.path.join(
            data_trasnformation_artifact_dir,
            data_transformation_config_info[TRANSFORMED_TRAIN_DIR_KEY])

        
            transformed_test_dir=os.path.join(
            data_trasnformation_artifact_dir,
            data_transformation_config_info[TRANSFORMED_TEST_DIR_KEY])

            preprocessing_object_file_path=os.path.join(
            data_trasnformation_artifact_dir,
            data_transformation_config_info[PREPROCESSING_DIR_KEY],
            data_transformation_config_info[PREPROCESSD_OBJECT_FILE_NAME_KEY])


            data_transformation_config=DataTransofrmationConfig(
                add_bedroom_per_room=add_bedroom_per_room,
                transformed_train_dir=transformed_train_dir,
                transformed_test_dir=transformed_test_dir, 
                preprocessing_object_file_path=preprocessing_object_file_path)
            
            logging.info(f'Data transformation config:{data_transformation_config}')

            return data_transformation_config



        except Exception as e:
            raise HousingException(e,sys) from e

    def get_model_trainer_config(self)->ModelTrainerConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir
            
            model_trainer_artifact_dir=os.path.join(artifact_dir,MODEL_EVALUATION_ARTIFACT_DIR,
            self.time_stamp)

            model_trainer_config_info= self.config_info[MODEL_TRAINER_CONFIG_KEY]
           
            trained_model_file_path = os.path.join(model_trainer_artifact_dir,
          #   model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],
             model_trainer_config_info[MODEL_TRAINER_MODEL_FILE_NAME_KEY])

            model_config_file_path= os.path.join(
                model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],
                model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY])

            base_accuracy=model_trainer_config_info[MODEL_TRAINER_BASE_ACCURACY_KEY]

            model_trainer_config= ModelTrainerConfig(
                trained_model_file_path=trained_model_file_path,
                base_accuracy=base_accuracy,
                model_config_file_path=model_config_file_path
            )

            logging.info(f"Model Trainer config {model_trainer_config}")

            return model_trainer_config
            
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        try:
            model_evaluation_config = self.config_info[MODEL_EVALUATION_CONFIG_KEY]
            artifact_dir = os.path.join(self.training_pipeline_config.artifact_dir,
                                        MODEL_EVALUATION_ARTIFACT_DIR, )

            model_evaluation_file_path = os.path.join(artifact_dir,
                                                    model_evaluation_config[MODEL_EVALUATION_FILE_NAME_KEY])
            response = ModelEvaluationConfig(model_evaluation_file_path=model_evaluation_file_path,
                                            time_stamp=self.time_stamp)
            
            
            logging.info(f"Model Evaluation Config: {response}.")
            return response
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def get_model_pusher_config(self) -> ModelPusherConfig:
        try:
            time_stamp = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
            model_pusher_config_info = self.config_info[MODEL_PUSHER_CONFIG_KEY]
            export_dir_path = os.path.join(ROOT_DIR, model_pusher_config_info[MODEL_PUSHER_MODEL_EXPORT_DIR_KEY],
                                           time_stamp)

            model_pusher_config = ModelPusherConfig(export_dir_path=export_dir_path)
            logging.info(f"Model pusher config {model_pusher_config}")
            return model_pusher_config

        except Exception as e:
            raise HousingException(e,sys) from e

    def get_trianing_pipeline_config(self)->TrainingPipelineConfig:
        
        try:
            training_pipeline_config=self.config_info[TRAINING_PIPELINE_CONFIG_KEY] #gets the group variable of pipeline
            artifact_dir=os.path.join(ROOT_DIR, training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            #this gives the path of the artifact folder
            #ROOT_DIR='d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\
            #TRAINING_PIPELINE_NAME_KEY=housing\\
            #TRAINING_PIEPLINE_ARTIFACT_DIT_KEY=artifact_dir'
            #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir
            #Check example.ipbynb for more details on how does this code works
            training_pipeline_config=TrainingPipelineConfig(artifact_dir=artifact_dir) #assigns value to config
            #entity strucutre of TrainingPipelineConfig
            logging.info(f'TrainingPieplineConfig: {training_pipeline_config}')
            return training_pipeline_config

        except Exception as e:
            raise HousingException(e,sys) from e
     