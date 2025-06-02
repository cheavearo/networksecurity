from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetwortSecurityException

### Configure of the Data Ingestion Config

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifacts_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
### Upgrade pymongo in Command Prompt: pymongo-4.13.0
import pymongo
from collections.abc import MutableMapping
from typing import List
from sklearn.model_selection import train_test_split

### The first step is to read data from MongoDB Database

from dotenv import load_dotenv
load_dotenv()

MONG_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetwortSecurityException(e,sys)
    
    def export_collection_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collecction_name
            self.mongo_client=pymongo.MongoClient(MONG_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            df =pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"], axis=1)
            df.replace({"na":np.nan}, inplace=True)
            return df

            
        except Exception as e:
            raise NetwortSecurityException(e,sys)
    
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            ## Create folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetwortSecurityException(e,sys)
    
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set,test_set=train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performing train_test split the dataframe")
            logging.info("Exited split_data_as_train_test method as DataIngestion class")
            ## Making train_test directory
            dir_path=os.path.dirname(self.data_ingestion_config.data_training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info("Export train test and test file path")
            ## Convert training set and test set to csv format
            train_set.to_csv(
                self.data_ingestion_config.data_training_file_path, index=False, header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.data_test_file_path, index=False, header=True
            )
            logging.info("Exporting train and test file path")
        except Exception as e:
            raise NetwortSecurityException(e,sys)
    
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(train_file_path=self.data_ingestion_config.data_training_file_path,
                                                        test_file_path=self.data_ingestion_config.data_test_file_path)
            return dataingestionartifact

        except Exception as e:
            raise NetwortSecurityException(e,sys)