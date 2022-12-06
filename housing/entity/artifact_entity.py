from collections import namedtuple


DataIngestionArtifact=namedtuple('DataIngestionArtifact',["train_file_path",
"test_file_path","is_ingested","message"])

#["train_file_path", location of the training data set 
#"test_file_path",   locoation of the test data set
# "is_ingested",     whether the data ingested successfully or not
# "message"])        Some messages we can pass


DataValidationArtifact=namedtuple('DataValidationArtifact',["schema_file_path","report_file_path",
"report_page_file_path","is_validated","message"])

DataTransformationArtifact=namedtuple('DataTransformationArtifact',[
    "preprocessing_object_file_path","transformed_train_file_path","transformed_test_file_path",
    "is_transformed","message"])


ModelTrainerArtifact = namedtuple("ModelTrainerArtifact", ["is_trained", "message", "trained_model_file_path",
                                                           "train_rmse", "test_rmse", "train_accuracy", "test_accuracy",
                                                           "model_accuracy"])