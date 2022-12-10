from collections import namedtuple

# This config entity file provides the skeleten structure variable for the input 
# configuration details required by each component. This structure does not 
# carry any value, value will be passed to this structure throgh configuration.py
# code which reads the config.yaml file to get the required value.
DataIngestionConfig=namedtuple("DataIngestionConfig",
                                [
                                    "dataset_download_url",
                                    "tgz_download_dir",
                                    "raw_data_dir",
                                    "ingested_train_dir",
                                    "ingested_test_dir"
                                ]
                             )

#"dataset_download_url", #URL of the input data source
#"tgz_download_dir",     #tgz is the zip file format, here we specify where the zipped input
#                        data to be downloaded that folder path or name we specify
# "raw_data_dir",        #Folder name where our extracted input data to be stored
# "ingested_train_dir",  #Folder name where our train data set to be stored
# "ingested_test_dir"    #Foldre nema where our test data set will be stored.
DataValidationConfig=namedtuple("DataValidationConfig",
                                [
                                    "schema_file_path",
                                    "report_file_path",\
                                    "report_page_file_path"
                                ]
                            )


#"schema_file_path" #specifying the location of where is my schema file stored 
#                   which can be used for validation of injested data set.
#"report_page_file_path" for saving some graph files
DataTransofrmationConfig=namedtuple("DataTransformationConfig",
                                    [
                                        "add_bedroom_per_room", 
                                        "transformed_train_dir",
                                        "transformed_test_dir",
                                        "preprocessing_object_file_path"
                                    ]
                                )

#["add_bedroom_per_room",  #Currently there is no beroom_per_room column is not there in my 
#                        data set. I will pass the value of this "add_bedroom_per_room" as
#                        True if I want to add a newcolumn for it otherwise I will pass 
#                        value as False
# "transformed_train_dir", #specifying the file location for my transforemed training file
#                          # where it will get stored
# "transformed_test_dir",#Specifying the file location for my test data transformed file
# "preprocessing_object_file_path"]) #Specifying the location of wher my trasnformed pickle
#                                    object will be stored


ModelTrainerConfig=namedtuple("ModelTrainerConfig",
                                [
                                    "trained_model_file_path",
                                    "base_accuracy",
                                    "model_config_file_path"
                                ]
                            )

#"trained_model_file_path", #Location of the pickled file created during model training
#"base_accuracy"            #supplying the expected accuracy of the model we are building
                            #We will not accept the model if the accuracy of the model is 
                            #less than the base accuracy.

                            #If are creating multiple model, we create pickle file for only
                            #one model which is performing best among them. we do not care 
                            #about other models. so we specify only one file path

ModelEvaluationConfig=namedtuple("ModelEvaluationConfig",
                                    [
                                        "model_evaluation_file_path",
                                        "time_stamp"
                                    ]
                                )

#"model_evaluation_file_path", #we are going to keep the information of our models,
                               #i.e. all the models which exists in production.
                        #During model evaluation we use model test data to evaluate our model
            #and we compare the model accuracy of new model with the old model which is 
            #already exist in the production, to get the beset model among them. But we need
            #information about the model which is present is production, that information we
            #will get through model evaluation file path. This file basically have information
            #of the all the models which are present in the production.
#"time_stamp" #This is the time stamp of the when the new model got compared with the old 
              # model. This is not part of data versioning. it is just model comparision time
              #stamp.

#This configuration set up will change or become more complex one based on your project.
#Here only the basic configuration setup we are doing as we are beginner

ModelPusherConfig=namedtuple("ModelPusherConfig",
                                [
                                    "export_dir_path"
                                ]
                            )

#"export_dir_path" # if our new model performing better than the olde model then we save
#                    that model in this path. This path is same as your production path where
#                    your old model present.

TrainingPipelineConfig= namedtuple("TrainingPipelineConfig",
                                    [
                                        "artifact_dir"
                                    ]
                                ) 

#Above are the information required for the configuration. How we provide all these 
#information is upto us, we can hard code the values or we can store required information
#in some file(yaml, json, csv) or data base and read information from file or data base through which we can
# provide the inforation.

#Here we are going to create the yaml file to store all these inforation and read this
#yaml file to pass the information requied for the configuration setup.

#yaml is also a file where we can store the information just like csv, json file. But 
#how we store the data in yaml file is bit different. In csv we store the data in 
#tabular format, in json we store the data in key value pair.
#There is no force that you have to use yaml file, if you want to use csv you can use as well.
#Even you can use mongodb.

#yaml file is more readable. It is very easy to store the information in yaml file. When you
#read the yaml file it gives the output in json (key value pair format).

#Here in config set up , the code requires data, we are isolating the code and data.
#if we modify the data we need not to modify the code and vise versa.

#now we are going to write the yaml file under config folder to give the configuration 
#information and we write some code to read that yaml file.
















