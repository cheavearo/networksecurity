import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
'''
Note: certifi is a Python package that make
root of certifikit for a secure connection.
'''
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetwortSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetwortSecurityException(e,sys)
    
    def cv_to_json_convertor(self, file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetwortSecurityException
    
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.colleciton = collection
            self.records  = records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]

            self.colleciton=self.database[self.colleciton]
            self.colleciton.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetwortSecurityException(e,sys)

if __name__=='__main__':

    FILE_PATH="Network_Data\phisingData.csv"
    DATABASE="VEAROAI"
    Collection ="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.cv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records, DATABASE, Collection)
    print(no_of_records)

