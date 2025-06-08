import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifacts_entity import(
    DataValidationArtifact,
    DataTransformationArtifact
)  
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetwortSecurityException
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact: DataValidationArtifact=data_validation_artifact
            self.data_transformation_config: DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise NetwortSecurityException(e,sys)
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetwortSecurityException(e,sys)

        
    def get_data_transformer_object(cls)->Pipeline:

        '''
        It initiates a KNNImputer Object with the parameters specified in the training pipeline.py file
        and returns a Pipeline object with KNNImputer object as the first step
        
        Args:
            cls: DataTransformation
            
        Returns:
           A Pipeline object
        '''
        logging.info("Starting get_data_transformation_object method of DataTransformation class")
        try:
            imputer: KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            ### **: means inserting key value pair of DATA_TRANSFORMATION_IMPUTER_PARAM
            logging.info(
            f"Initiate the KNNimputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
        )
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetwortSecurityException(e,sys)
    
    def initiate_data_transformation(self)->DataTransformationArtifact:

        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting Data Transformation")
            
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)


            # Training the dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df= target_feature_train_df.replace(-1,0)

            # Test dataframe
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df= target_feature_test_df.replace(-1,0)

            # Impute np.nan by KNNImputer
            preprocessor=self.get_data_transformer_object()
            preprocessor_obj=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor_obj.transform(input_feature_test_df)
            #### Note: no need to apply 'fit' method to test data to avoid information leaking 

            train_arr = np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]

            # Save numpy array data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_obj)

            save_object( "final_model/preprocessor.pkl",preprocessor_obj)

            # Preparing the artifacts of Data Transformation
            data_transformation_artifact=DataTransformationArtifact(
            transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
            transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
            transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
            return data_transformation_artifact
            #This are what expected to return of DataTransformation class

        except Exception as e:
            raise NetwortSecurityException(e,sys)
                 

            