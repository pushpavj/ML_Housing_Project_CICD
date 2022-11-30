from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.configuration import Configuration
from housing.component.C_data_transformation import DataTransformation
import os, sys



def main():
    try:
        pipeline=Pipeline()
        pipeline.run_pipeline()
        # datavalidationconfig=Configuration().get_data_validation_config()
        # print(datavalidationconfig)
        # datatransformationconfig=Configuration().get_data_transformation_config()
        # print(datatransformationconfig)
        # file_path=r"D:\user\jupyternotes\Praketh\pycharmforpractice\ML_Housing\ML_Housing_Project_CICD\housing\artifact\data_ingestion\2022-11-28-19-51-27\ingested_data\train\housing.csv"
        # schema_file_path=r"D:\user\jupyternotes\Praketh\pycharmforpractice\ML_Housing\ML_Housing_Project_CICD\config\schma.yaml"
        # df=DataTransformation.load_data(file_path,schema_file_path)
        # print(df.dtypes)
    except Exception as e:
        raise HousingException(e,sys) from e

if __name__=="__main__":
    main()
