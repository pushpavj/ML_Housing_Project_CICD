import os,sys
from datetime import datetime
ROOT_DIR=os.getcwd()  # to get current working directory

print('root Dir is', ROOT_DIR)
CONFIG_DIR="config"
CONFIG_FILE_NAME="config.yaml"
CONFIG_FILE_PATH=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

print('CONFIG_FILE_PATH=', CONFIG_FILE_PATH)
#The file path we are creating dynamically here, because the code can work in any system, 
#If you hardcode the path the code may work fine in your local system but it may not work in
#any other system.

CURRENT_TIME_STAMP=f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

#Training pipeline related variables
TRAINING_PIPELINE_CONFIG_KEY='training_pipeline_config' #this should be exact name we have in yamlfile
TRAINING_PIPELINE_ARTIFACT_DIR_KEY='artifact_dir' #same as what we have in yaml file
TRAINING_PIPELINE_NAME_KEY='pipeline_name' #should be saem as what we have in yaml file

#Data ingetion related variables for each of the variables we defined in yaml file
DATA_INGESTION_ARTIFACT_DIR='data_ingestion'
DATA_INGESTION_CONFIG_KEY='data_ingestion_config'
DATASET_DOWNLOAD_URL_KEY='dataset_download_url'
RAW_DATA_DIR_KEY='raw_data_dir'
TGZ_DOWNLOAD_DIR_KEY='tgz_download_dir'
INGESTED_DIR_KEY='ingested_dir'
INGESTED_TRAIN_DIR_KEY='ingested_train_dir'
INGESTED_TEST_DIR_KEY='ingested_test_dir'

#Data validation variables 
DATA_VALIDATION_CONFIG_KEY='data_validation_config'
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY='schema_file_name'
DATA_VALIDATION_SCHEMA_DIR_KEY='schema_dir' 
DATA_VALIDATION_ARTEFACT_DIR_NAME_KEY="data_validation"
DATA_VALIDATION_REPORT_FILE_NAME_KEY="report_file_name"
DATA_VALIDATION_REPROT_PAGE_FILE_NAME_KEY="report_page_file_name"

#data transformation variables
DATA_TRANSFORMATION_ARTIFACT_DIR_KEY='data_transformation'
DATA_TRANSFORMATION_CONFIG_KEY='data_transformation_config'
ADD_BEDROOM_PER_ROOM_KEY='add_bedrooom_per_room'
TRANSFORRMED_DIR_KEY='transformed_dir'
TRANSFORMED_TRAIN_DIR_KEY='transformed_train_dir'
TRANSFORMED_TEST_DIR_KEY='transformed_test_dir'
PREPROCESSING_DIR_KEY='preprocessing_dir'
PREPROCESSD_OBJECT_FILE_NAME_KEY='preprocessed_object_file_name'

#model trainer variables
MODEL_TRAINER_CONFIG_KEY='model_trainer_config'
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY='trained_model_dir'
MODEL_TRAINER_MODEL_FILE_NAME_KEY='model_file_name'
MODEL_TRAINER_BASE_ACCURACY_KEY='base_accuracy'
MODEL_TRAINER_ARTIFACT_DIR='model_trainer'
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY= 'model_config_dir'
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY='model_config_file_name'






#model evaluation variables
MODEL_EVALUATION_CONFIG_KEY='model_evaluation_config'
MODEL_EVALUATION_FILE_NAME_KEY='model_evaluation_file_name'
MODEL_EVALUATION_ARTIFACT_DIR='model_evaluation'

#model pusher variables
MODEL_PUSHER_CONFIG_KEY='model_pusher_config'
MODEL_PUSHER_MODEL_EXPORT_DIR_KEY='model_export_dir'

BEST_MODEL_KEY='best_model'
HISTORY_KEY='history'
MODEL_PATH_KEY='model_path'

EXPERIMENT_DIR_NAME='experiment'
EXPERIMENT_FILE_NAME='experiment.csv'



COLUMN_TOTAL_ROOMS = "total_rooms"
COLUMN_POPULATION = "population"
COLUMN_HOUSEHOLDS = "households"
COLUMN_TOTAL_BEDROOM = "total_bedrooms"
DATASET_SCHEMA_COLUMNS_KEY=  "columns"

NUMERICAL_COLUMN_KEY="numerical_columns"
CATEGORICAL_COLUMN_KEY = "categorical_columns"
TARGET_COLUMN_KEY="target_column"