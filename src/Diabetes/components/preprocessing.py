import pandas as pd
import os,sys
from dataclasses import dataclass
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logger import logging
from imblearn.over_sampling import SMOTE
from src.utils import save_obj,get_balance_dataset
from imblearn.under_sampling import RandomUnderSampler

@dataclass
class preprocessorCofig:
    preprocessor_path_config:str = os.path.join('artifacts/Diabetes_models','diabestes_preprocessor.pkl')

class PreProcessing:
    def __init__(self) -> None:
        self.preprocessor_path = preprocessorCofig()

    def get_data_transformed_obj(self,df):
       
        try:
            cat_col = df.select_dtypes(include=object)
            cat_col = list(cat_col)
            cat_pipeline = Pipeline([
                ('ohe',OneHotEncoder(drop='first'))
            ])
            preprocessor = ColumnTransformer([
                ('cat',cat_pipeline,cat_col)
            ],remainder='passthrough')
            
            return preprocessor 
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,df):
        ##do train test split
        try:
            preprocessor_obj = self.get_data_transformed_obj(df)
            
            


            #Down sampleing
            X = df.drop(columns=['diabetes'],axis='columns')
            y = df['diabetes']
            logging.info(X.columns)
            rus = RandomUnderSampler(random_state=42)
            X_res,y_res = rus.fit_resample(X,y) 
            logging.info(X_res.head(1))
            logging.info(X_res.columns)

            X_res.reset_index(drop=['index'],inplace=True)
            y_res.reset_index(drop=['index'],inplace=True)
            X_train,X_test,y_train,y_test = train_test_split(X_res,y_res,test_size=0.2,random_state=42)

            X_train_transformed = preprocessor_obj.fit_transform(X_train)
            X_test_transformed = preprocessor_obj.transform(X_test)
            save_obj(file_path=self.preprocessor_path.preprocessor_path_config,obj=preprocessor_obj)
            
            logging.info("Train test complited")
            
            return X_train_transformed,X_test_transformed,y_train,y_test
        
        except Exception as e:
            raise CustomException(e,sys)