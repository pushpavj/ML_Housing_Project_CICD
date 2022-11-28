from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.configuration import Configuration
import os, sys



def main():
    try:
        pipeline=Pipeline()
        pipeline.run_pipeline()
        # datavalidationconfig=Configuration().get_data_validation_config()
        # print(datavalidationconfig)

    except Exception as e:
        raise HousingException(e,sys) from e

if __name__=="__main__":
    main()
