from aifc import Error
from housing.config.configuration import Configuration
from housing.logger import logging
from housing.exception import HousingException
import os,sys

from housing.entity.artifact_entity import DataIngestionArtifact
from housing.entity.config_entity import DataIngestionConfig
from housing.component.A_data_ingestion import DataIngestion

class Pipeline:

    def __init__(self,config:Configuration=Configuration()) -> None:
        # creates the object of Configuration() (which reads the config.yaml file
        # and assigns the value to configuration entity)
        try:
            self.config=config 
        except Exception as e:
            raise HousingException(e,sys) from e


    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
        # this function first calls the config.get_data_ingestion_config() and
        #gets the data ingestion config entity variable values from config.yaml.
        #Then DataIngestion class from data ingestion component library 
        # with passing the configuration entity variable values.
        # Then calls the initiate_data_ingestion() function from Dataingestion 
        #component.
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
       #gets and  #Returns the data_ingestion_artifact entity output variables
# as path of train and test files, status of ingested and successfull message 

        
        except Exception as e:
            raise HousingException(e,sys) from e

    def start_data_validation(self)->DataValidationArtifact:
      
        try:
            data_validation=DataValidation(data_validation_config=self.config.get_data_validation_config())
            return data_validation.initate_data_validation()
        
        except Exception as e:
            raise HousingException(Error,sys) from e


    def start_data_transformation(self)->DataTransformationArtifact:
        try:
            data_transformation=DataTransformation(data_transformation_config=self.config.get_data_transformation_config())
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise HousingException(Error,sys) from e



    def start_model_trainer(self)->ModelTrainerArtifiact:
        try:
            model_trainer=ModelTrainer(model_trainer_config=self.config.get_model_trainer_config())
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise HousingException(Error,sys) from e


    def start_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            model_evaluation=ModelEvaluation(model_evaluation_config=self.config.get_model_evaluation_config())
            return model_evaluation.initiate_model_trainer()
        
        except Exception as e:
            raise HousingException(Error,sys) from e

 
    def start_model_pusher(self)->ModelPusherArtifact:
        try:
            model_pusher=ModelPusher(model_pusher_config=self.config.get_model_pusher_config())
            return model_pusher.initiate_model_pusher()        
        except Exception as e:
            raise HousingException(Error,sys) from e

        
    def run_pipeline(self):
        try:
            #data ingestion
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation()
            data_transoformation_artifact=self.start_data_transformation()
            data_model_trainer=self.start_data_model_trainer()
            data_model_evaluation=self.start_data_model_evaluation()
            data_model_pusher=self.start_model_pusher()
        except Exception as e:
            raise HousingException(e,sys) from e


