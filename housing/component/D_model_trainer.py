from housing.logger import logging
from housing.exception import HousingExcpetion
from housing.config.configuration import Configuration
from housing.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact
from housing.entity.config_entity import ModelTrainerConfig
import os,sys
from housing.constant import *
from housing.util.util import read_yaml_file,load_numpy_array_data,save_object,load_object
import yaml
import importlib 
from housing.entity.model_factory import MetricInfoArtifact, ModelFactory,GridSearchedBestModel
from housing.entity.model_factory import evaluate_regression_model


class HousingEstimatorModel:
    def __init__(self,preprocessing_object,trained_model_object):
        """
        Trained Model constructor
        preprocessing object: preprocessing_object
        trained_model_object: trained_model_object
        """

        self.preprocessing_objects=preprocessing_object
        self.trained_model_object=trained_model_object
    
    def predict(self,X):
        """
        function accepts raw input and then transformed raw input using preprocessing_object
        which guarantees that tha inputs are in the same format as the training data.
        At last it peroforms prediction on the transformed features
        """

        transfored_feature= self.preprocessing_objects.transform(X)
        return self.trained_model_object.predict(transfored_feature)
    
    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


class ModelTrainer():
    def __init__ (self, model_trainer_config:ModelTrainerConfig,
        data_transformation_artifact:DataTransformationArtifact):

        try:
            logging.info(f"{'>>' *30} Model Trainer log started {'<<' *30 } ")
            self.model_trainer_config=model_trainer_config
            self.data_transofmation_artifact= data_transformation_artifact

        except Exception as e:
            raise HousingExcpetion(e,sys) from e

    def initiate_model_trainer(self)->ModelTrainerArtifact:

        try:
            logging.info(f"Loading transformed trainig data set")
            transoformed_training_file_path=self.data_transofmation_artifact.transformed_test_file_path
            train_array=load_numpy_array_data(file_path=transoformed_training_file_path)

            logging.info(f"Loading transformed testing data set")
            transformed_test_file_path= self.data_transofmation_artifact.transformed_test_file_path
            test_array=load_numpy_array_data(file_path=transformed_test_file_path)

            logging.info(f"Splitting training and testing input and target feature")
            x_train=train_array[:,:-1] #including all feature with excluding last feature
            y_train=train_array[:,-1] #including only the last feature
            x_test=test_array[:,:-1]#including all feature with excluding last feature
            y_test=test_array[:,-1]#including only the last feature

            logging.info(f"Extracting model config file path")
            model_config_file_path=self.model_trainer_config.model_config_file_path

            logging.info(f"Initializing the model factory class using above config file:{model_config_file_path}")
            model_factory=ModelFactory(model_config_file_path=model_config_file_path)
            
            base_accuracy=self.model_trainer_config.base_accuracy

            logging.info("Expected accuracy: {base_accuracy}")
            
            logging.info("Intiating the operation model selection")
            best_model=model_factory.get_best_model(X=x_train,y=y_train,base_accuracy=base_accuracy)

            logging.info(f"Best model found on training data set: {best_model}")

            logging.info(f"Extracting trained model list")
            grid_searched_best_model_list: List[GridSearchedBestModel]=model_factory.grid_searched_best_model_list

            model_list=[model.best_model for model in grid_searched_best_model_list]

            logging.info(f"Eavaluation of all trained model on training and testing dataset both")
            metric_info:MetricInfoArtifact=evaluate_regression_model(model_list=model_list,
            X_train=x_train,y_train=y_train)

            logging.info(f"Best found model on both training and testing dataset")

            preprocssing_obj=load_object(file_path=self.data_transofmation_artifact.preprocessing_object_file_path)
            model_object=metric_info.model_object

            trained_model_file_path=self.model_trainer_config.trained_model_file_path
            housing_model=HousingEstimatorModel(preprocssing_object=preprocssing_obj,trained_model_object=model_object)
            logging.info(f"Saving model at  path : {trained_model_file_path}")

            save_object(file_path=trained_model_file_path,obj=housing_model)

            model_trainer_artifact=ModelTrainerArtifact(is_trained=True,
            message="Model Trained Successfully",
            trained_model_file_path=trained_model_file_path,
            train_rmse=metric_info.train_rmse,
            test_rmse=metric_info.test_rmse,
            train_accuracy=metric_info.train_accuracy,
            model_accuracy=metric_info.model_accuracy)

            logging.info(f"Model traiing successfull: {model_trainer_artifact}")

            return model_trainer_artifact
        
        except Exception as e:
            raise HousingExcpetion(e,sys) from e

    def __del__(self):
        logging.info(f"{'<<'*30} Model trainer log completed {'<<'*30}")

        

#loading transformed training and testing data set
#reading model config file
#getting best model on both trainiing data set
#evaluating models on both training and data set and getting model object
#loading prprocessing object

#custome model object by combining both prprocessin object and model object
#saving custome model object
#returning model trainer artifact




       

