from housing.logger import logging
from housing.exception import HousingException
from housing.config.configuration import Configuration
from housing.entity.config_entity import DataTransofrmationConfig
from housing.entity.artifact_entity import DataTransformationArtifact,\
DataIngestionArtifact,DataValidationArtifact
import os, sys
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from housing.util.util import read_yaml_file
from housing.util.util import save_numpy_array_data,save_object,load_numpy_array_data,load_object

COLUMN_TOTAL_ROOMS='total_rooms'
COLUMN_POPULATION='population'
COLUMN_HOUSEHOLDS='households'
COLUMN_TOTAL_BEDROOM='total_bedrooms'
DATASET_SCHEMA_COLUMNS_KEY='columns'
NUMERICAL_COLUMNS_KEY='numerical_columns'
CATEGORICAL_COLUMNS_KEY='categorical_columns'
TARGET_COLUMN_KEY='target_column'


class FeatureGenerator(BaseEstimator,TransformerMixin):


    def __init__(self,add_bedrooms_per_room=True,
                 total_room_ix=3,
                 population_ix=5,
                 households_ix=6,
                 total_bedrooms_ix=4, columns=None):


        """ 
            FeatureGenerator initialization
            add_bedrooms_per_room: bool
            total_room_ix:int index number of total_rooms columns
            population_ix:int index number of population columns
            households_ix:int index number of households columns
            total_bedrooms_ix:int index number of total_bedrooms columns
        """

        try:
            self.columns=columns
           # self.add_bedrooms_per_room=add_bedrooms_per_room
            if self.columns is not None:
                total_room_ix=self.columns.index(COLUMN_TOTAL_ROOMS)
                population_ix=self.columns.index(COLUMN_POPULATION)
                households_ix=self.columns.index(COLUMN_HOUSEHOLDS)
                total_bedrooms_ix=self.columns.index(COLUMN_TOTAL_BEDROOM)
        
            self.add_bedrooms_per_room=add_bedrooms_per_room
            self.total_room_ix=total_room_ix
            self.population_ix=population_ix
            self.households_ix=households_ix
            self.total_bedrooms_ix=total_bedrooms_ix
        except Exception as e:
            raise HousingException(e,sys) from e


    def fit(self,X,y=None):

        return self 

    def transform(self, X, y=None):
        try:
            room_per_household=X[:,self.total_room_ix]/ X[:,self.households_ix]
            population_per_household=X[:,self.population_ix]/X[:,self.households_ix]

            if self.add_bedrooms_per_room:
                bed_rooms_per_room=X[:,self.total_bedrooms_ix]/X[:,self.total_room_ix]
            
                generated_feature=np.c_[X,room_per_household,population_per_household,bed_rooms_per_room]
            else:
                generated_feature=np.c_[X,room_per_household,population_per_household]

            return generated_feature

        except Exception as e:
            raise HousingException(e,sys) from e




class DataTransformation:

    def __init__(self,data_transformation_config:DataTransofrmationConfig,
    data_ingestion_artifact:DataIngestionArtifact,
    data_validation_artifact:DataValidationArtifact):

        try:
            self.data_transformation_config= data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e 
    @staticmethod
    def load_data(file_path:str,schema_file_path:str)->pd.DataFrame:

        """
        This function will checks for the data type of each column specified inside the
        schema file and performs the type casting to the actual data we are getting accordingly
        
        It reads the column name from the schema.yaml file and then reads the data type,
        using this data type it apply the type casting to the column specified in the given data set
        """
        try:
            dataset_schema=read_yaml_file(schema_file_path)
            schema_columns=dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]
          #  print(schema)

            data_frame=pd.read_csv(file_path)
            error_message=" "

            for i in data_frame.columns:
                if i in list(schema_columns.keys()):
                    data_frame[i].astype(schema_columns[i])
                else:
                    error_message=f"{error_message} \n column: [{i}] is not in the schema."
                #print(error_message)
            return data_frame
        except Exception as e:
            raise HousingException(e,sys) from e

 
    def get_data_transformer_object(self)->ColumnTransformer:
        try:
            schema_file_path=self.data_validation_artifact.schema_file_path
            dataset_schema=read_yaml_file(schema_file_path)
            numerical_columns=dataset_schema[NUMERICAL_COLUMNS_KEY]
            categorical_columns=dataset_schema[CATEGORICAL_COLUMNS_KEY]


 # The transformation we apply for numerical column is different from what we apply for categorical
#columns. At the end we will cobine the transformed numerical columns with the transformed categorical 
#columns

#first we create numerical pipeline
#All the feature engineering steps for numerical feature we can combine in single

            num_pipeline=Pipeline(steps=[('imputer',SimpleImputer(strategy="median")),
            ('feature_generator',FeatureGenerator(
                add_bedrooms_per_room=self.data_transformation_config.add_bedroom_per_room,
                columns=numerical_columns
            )),
            ('scaling',StandardScaler())])

            #Now create seperate pipeline for categorical pipeline
            cat_pipeline=Pipeline(steps=[('imputer',SimpleImputer(strategy='most_frequent')),
            ('onehotencoder',OneHotEncoder()),
            ('scaling',StandardScaler(with_mean=False))])

            logging.info(f"Categorical columns{categorical_columns}")
            logging.info(f"Numerical columns{numerical_columns}")

            # numerical_column_name=['longitude', 'latitude', 'housing_median_age',
            #  'total_rooms',
            #     'total_bedrooms', 'population', 'households', 'median_income',]
            # cat_column_name=["ocean_proximity"]
            #now let us create the preprocessing pickle object


            preprocessing= ColumnTransformer([('num_pipeline',num_pipeline,numerical_columns),
            ('cat_pipeline',cat_pipeline,categorical_columns)])
            return preprocessing

            

        except Exception as e:
            raise HousingException(e,sys) from e   



    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            logging.info(f"Obtaining preprocessing object")
            preprocessing_obj= self.get_data_transformer_object()
            
            logging.info(f"Obtaining training and test file path")
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            schema_file_path=self.data_validation_artifact.schema_file_path
            
            logging.info(f"Loading training and test data as pandas data frame")
            train_df=self.load_data(file_path=train_file_path,
                        schema_file_path=schema_file_path)
            test_df=self.load_data(file_path=test_file_path,
                        schema_file_path=schema_file_path)

            schema=read_yaml_file(schema_file_path)
            target_column= schema[TARGET_COLUMN_KEY]
            
            logging.info(f"Splitting input and target feature from training and testing df")
            input_feature_train_df= train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df=train_df[target_column]

            input_feature_test_df=test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df=test_df[target_column]
            

            logging.info(f"Applying preprocessing object on train and test df")
            input_feature_train_array=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_array=preprocessing_obj.transform(input_feature_test_df)

            train_array=np.c_[input_feature_train_array,target_feature_train_df]
            test_array=np.c_[input_feature_test_array,target_feature_test_df]

            transformed_train_dir=self.data_transformation_config.transformed_train_dir
            transformed_test_dir=self.data_transformation_config.transformed_test_dir

            train_file_name=os.path.basename(train_file_path).replace('.csv','.npz')
            test_file_name=os.path.basename(test_file_path).replace('.csv','.npz')
            #the file name got created is of .csv here. but for numpy array we need to 
            #give file extention as npz

            transformed_train_file_path=os.path.join(transformed_train_dir,train_file_name)
            transformed_test_file_path=os.path.join(transformed_test_dir,test_file_name)
            
            logging.info(f"Saving transformed train and test arrays")

            save_numpy_array_data(file_path=transformed_train_file_path,array=train_array)
            save_numpy_array_data(file_path=transformed_test_file_path,array=test_array)
     
            preprocessing_obj_file_path=self.data_transformation_config.preprocessing_object_file_path
            
            logging.info(f'Saving preprocessing object ')
            save_object(file_path=preprocessing_obj_file_path,obj=preprocessing_obj)
            
            logging.info(f"Creating data trasnformation artifact ")
            data_transformation_artifact=DataTransformationArtifact(
            preprocessing_object_file_path=preprocessing_obj_file_path,
            transformed_train_file_path=transformed_train_file_path, 
            transformed_test_file_path=transformed_test_file_path, 
            is_transformed=True, 
            message="Data Transmission Successfull")

            

            logging.info(f"Data transformation artifact{data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e