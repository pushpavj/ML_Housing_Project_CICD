from housing.logger import logging
from housing.exception import HousingException
import os, sys
from housing.entity.config_entity import DataIngestionConfig 
from housing.entity.artifact_entity import DataIngestionArtifact
import tarfile
from six.moves import urllib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit


class DataIngestion:
#This class is called by pipeline.py with passing the data ingestio configuration
# entity variable values.
#Then assingns this data entity config variable values to the data_ingestion_config
#as below
# config Variable name     #value content description
#"dataset_download_url", #URL of the input data source
#"tgz_download_dir",     #tgz is the zip file format, here we specify where the zipped input
#                        data to be downloaded that folder path or name we specify
# "raw_data_dir",        #Folder name where our extracted input data to be stored
# "ingested_train_dir",  #Folder name where our train data set to be stored
# "ingested_test_dir"    #Foldre nema where our test data set will be stored.
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
        #This module will accept the configure entity structure with values
        # from Pipe line module
            logging.info(f"{'='*20} Data Ingestion log started.{'='*20}")
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def download_housing_data(self):
    #This function is called by initiate_data_ingestion function in this module
    #itself.

        try:
            #gets the remote url to download dataset from configuration details
            download_url=self.data_ingestion_config.dataset_download_url
#https://raw.githubusercontent.com/ageron/handson-ml/master/dataset/housing/housing.tgz
            #folder location to download zip file
        #the path is as below
    #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\raw_data\\tgz_data
            tgz_download_dir=self.data_ingestion_config.tgz_download_dir

#Checks if the above directory already exist, if yes then remove it
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)
#Then create the tgz_data directory using the above file path
            os.makedirs(tgz_download_dir,exist_ok=True)

#Get just file name housing.tgz from the below url
#https://raw.githubusercontent.com/ageron/handson-ml/master/dataset/housing/housing.tgz
            housing_file_name=os.path.basename(download_url)
#create the new path to save tgz_file housing.tgz.
##d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\raw_data\\tgz_data\\housing.tgz
            tgz_file_path=os.path.join(tgz_download_dir,housing_file_name)

            logging.info(f'Downloading file from [{download_url} into {tgz_file_path}]')
#Now download the file housing.tgz from download url and place it in above newly
#created path
            urllib.request.urlretrieve(download_url,tgz_file_path)
            

            logging.info(f'File {tgz_file_path} has been downloaded successfully')
            print('tgz_file_path',tgz_file_path)

            return tgz_file_path 
#returns only the path details where the zipped data set is saved i.e
##d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\raw_data\\tgz_data\\housing.tgz

        
        except Exception as e:
            raise HousingException(e,sys) from e

    def extract_tgz_file(self,tgz_file_path:str):
#This function is called by initiate_data_ingestion function in this module
    #itself with passing the tgz_file_path as below
##d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\raw_data\\tgz_data\\housing.tgz

#This module create the raw_data_dir folder and extract the tgz file present in 
# the tgz_data folder and saves the extracted file in the raw_data_dir  folder
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir
 #Gets the raw_data_dir path as below 
 # #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\raw_data           
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir)
#creates teh raw_data_dir as below
#d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\raw_data
            logging.info(f'Extracting tgz file {tgz_file_path} into dir {raw_data_dir}')
            print("TAR file path",tgz_file_path)
            housing_tgz_file_obj=tarfile.open(tgz_file_path)
#Gets the zipped file path as below
##d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\raw_data\\tgz_data\\housing.tgz
            housing_tgz_file_obj.extractall(path=raw_data_dir)
#Extracted file is placed under below path
#d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\raw_data
            logging.info(f'Extraction completed')

        except Exception as e:
            raise HousingException(e,sys) from e

    def split_data_as_train_test(self):
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir
#Gets the path of raw_data_dir
#d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\raw_data
            file_name=os.listdir(raw_data_dir)[0]
#selects the 0th file name inside the raw_dat folder i.e extracted file name here

            housing_file_path=os.path.join(raw_data_dir,file_name)
#creates the extracted file path as below
#d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\raw_data\\housing.csv
            logging.info(f'Reading CSV file:[{housing_file_path}]')
#reading the csv file housing.csv present in the raw_data folder
            housing_data_frame=pd.read_csv(housing_file_path)

#creates the new column as income_cat and gets the value for this from the 
#median_income (which is having continuous value) and it is being categorized
#into 5 catgories based on the bin width provided. So the catgories will be
#stored inside the new column income_cat
            housing_data_frame['income_cat']=pd.cut(
                housing_data_frame['median_income'], 
                bins=[0.0,1.5,3.0,4.5,6.0,np.inf],
                labels=[1,2,3,4,5]

            )
#The intention of categorizing the data based on median_income is that,
#When we are splitting the data set for train and test, we want to make 
#sure that the propornality of each categories should be same in train and 
#test data. This is to ensure that there should not be any imbalance is the
#data or there should not be any biase in the data splitting, i.e. all categories
#data should be present in both train and test data set. To ensure this we use
#Stratified split method this ensures all the categories should be present
#in both train and test data and in the same proportion. Means if we 
#draw a pi chart for original data, then for train data and and then
#for test data it should show the same proportinaliry for all the three.
            logging.info(f'Splitting data into train and test data set')
            strat_train_set=None
            strat_test_set=None

            split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)

            for train_index,test_index in split.split(housing_data_frame,housing_data_frame['income_cat']):
                strat_train_set=housing_data_frame.loc[train_index].drop('income_cat',axis=1)
                strat_test_set=housing_data_frame.loc[test_index].drop('income_cat',axis=1)
#Here we are dropping the income_cat column for in train and test data set as 
# this was the new column we added just to get the categories and by using those
# categories the stratified split can happen. 
            train_file_path=os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)
#here forming the file path for training data set as below
#d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\ingested_data\\train\\housing.csv
            test_file_path=os.path.join(self.data_ingestion_config.ingested_test_dir,
                                            file_name)
#d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\ingested_data\\test\\housing.csv                                      
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
#creating the train folder as below
#d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\ingested_data\\train\\housing.csv
                logging.info(f'Exporting training dataset to file:[{train_file_path}]')
                strat_train_set.to_csv(train_file_path,index=False)
#Saving the train data set in below path
#d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\ingested_data\\train\\housing.csv
            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
#creating the test file with below path
# #d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\ingested_data\\test\\housing.csv                  
                logging.info(f'Exporting test dataset to file:[{test_file_path}]')
                strat_test_set.to_csv(test_file_path,index=False)
#saving the test file with below path
#d:\\user\\jupyternotes\\Praketh\\pycharmforpractice\\ML_Housing\\ML_Housing_Project_CICD\\housing\\artifact_dir//da
    #ta_ingetion\\timestampMMDDYYHHMMSS\\ingested_data\\test\\housing.csv  
            data_ingestion_artifact=DataIngestionArtifact(train_file_path=train_file_path,
            test_file_path=test_file_path,
            is_ingested=True,
            message=f'Data ingestion completed succssfully'
            )
#Setting up the values for data_ingestion_artifact entity output variables
# as path of train and test files, status of ingested and successfull message 
            logging.info(f"Data Ingestion artifact: [{data_ingestion_artifact}]")

            return data_ingestion_artifact
#Returns the data_ingestion_artifact entity output variables
# as path of train and test files, status of ingested and successfull message 

        except Exception as e:
            raise HousingException(e,sys) from e
    
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
    #This function is called by pipeline.py to initiate the data ingetion pipeline
    #component.
    #This function triggers the first tasks being performed by data ingestion 
    #component one by one.
    # i.e. 1) downloading the zipped housing data set
    # Gets the path of where zipped housing data set is saved.
    # 2)Passes the tgz zipped file saved path and 
    # Extracting the raw dataset from the zipped file
    #3) Splitting the raw data in to train and test data set.
    #Finally returns the output of split data as train and test function
    #i.e indirectly return data_ingestion_artifacts
    #data_ingestion_artifact=DataIngestionArtifact
    # (train_file_path=train_file_path,
            # test_file_path=test_file_path,
            # is_ingested=True,
            # message=f'Data ingestion completed succssfully')
        try:
            tgz_file_path=self.download_housing_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
    #Returns the data_ingestion_artifact entity output variables
# as path of train and test files, status of ingested and successfull message 
        except Exception as e:
            raise HousingException(e,sys) from e 

    def __del__(self):
        logging.info(f"{'='*20} Data ingetion log completed {'='*20} \n\n")


