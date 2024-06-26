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


@dataclass
class preprocessorCofig:
    preprocessor_path_config:str = os.path.join('artifacts/Diabetes','diabestes_preprocessor.pkl')

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
            
            

            X = df.iloc[:, :-1]  
            y = df.iloc[:, -1] 

            X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

            X_train_transformed = preprocessor_obj.fit_transform(X_train)
            X_test_transformed = preprocessor_obj.transform(X_test)
            save_obj(file_path=self.preprocessor_path.preprocessor_path_config,obj=preprocessor_obj)
            #X_train,X_test,y_train,y_test = train_test_split(X_resampled,y_resampled,test_size=0.2,random_state=42)
            logging.info("Train test complited")
            
            return X_train_transformed,X_test_transformed,y_train,y_test
        
        except Exception as e:
            raise CustomException(e,sys)