from collections import namedtuple


DataIngestionArtifact=namedtuple('DataIngestionArtifact',["train_file_path",
"test_file_path","is_ingested","message"])

#["train_file_path", location of the training data set 
#"test_file_path",   locoation of the test data set
# "is_ingested",     whether the data ingested successfully or not
# "message"])        Some messages we can pass


DataValidationArtifact=namedtuple('DataValidationArtifact',["schema_file_path","report_file_path",
"report_page_file_path","is_validated","message"])