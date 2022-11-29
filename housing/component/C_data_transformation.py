from housing.logger import logging
from housing.exception import HousingException
from housing.config.configuration import Configuration
from housing.entity.config_entity import DataTransofrmationConfig
from housing.entity.artifact_entity import DataTransformationArtifact,DataIngestionArtifact,DataValidationArtifact
import os, sys


class DataTransformation:

    def __init__(self,data_transformation_config:DataTransofrmationConfig,
    data_ingestion_artifact:DataIngestionArtifact,data_validation_artifact:DataValidationArtifact):

        try:
            self.data_transformation_config= data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e 
    def is_train_test_file_exists():
        try:
           pass

        except Exception as e:
          raise HousingException(e,sys) from e

    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            self.is_train_test_file_exists()
            self.transform_train_file()

        except Exception as e:
            raise HousingException(e,sys) from e