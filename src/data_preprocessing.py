import pandas as pd 
import numpy as np 
from sklearn.preprocessing import OneHotEncoder, LabelEncoder,OrdinalEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer,SimpleImputer
from src.feature_engineering import FeatureEngineering
from src.utils import read_csv

class DataPreprocessing:
    def __init__(self,csv_path):
        self.csv_path = csv_path
        self.df = None
        self.save_path = os.path.join("data/processed", "preprocessed.csv")

    def featureEngineering(self):
        fe = FeatureEngineering(csv_path=self.csv_path)
        logger.info("Object for feature engineering initiated")
        fe.voter_turnout()
        fe.vote_share()
        fe.get_pdi()
        fe.save()
        self.csv_path = os.path("data/processed/engineered.csv")
        self.df = read_csv(self.csv_path)

    @staticmethod
    def cat_transformer(self):
        cat_trans = Pipeline(steps=[
            ('imputer',SimpleImputer(strategy='most_frequent')),
            ("encoder",OneHotEncoder(handle_unknown='ignore'))
        ])
        return cat_trans

    @staticmethod
    def num_transformer(self):
        num_trans = Pipeline(steps=[
            ('imputer',KNNImputer(n_neighbors=5)),
            ("encoder",StandardScaler())
        ])
        return num_trans

    def PreprocessingPipeline(self):
        self.df = self.df.drop(columns=['pc_name', 'cand_name'])
        low_card_cat = ['st_name', 'pc_type', 'cand_sex']
        high_card_cat = ['partyname', 'partyabbre']
        numeric_cols = ['year', 'pc_no', 'totvotpoll', 'electors', 'voter_turnout', 'vote_share', 'pdi_x']
       
        for col in high_card_cat:
            freq_map = self.df[col].value_counts().to_dict()
            self.df[col + "_freq"] = self.df[col].map(freq_map)

        numeric_cols += [col + "_freq" for col in high_card_cat]

      
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', self.cat_transformer(), low_card_cat),
                ('num', self.num_transformer(), numeric_cols)
            ]
        )

        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor)
        ])
        logger.info("Preprocessing pipeline created successfully.")
        return pipeline
    def run(self):
        try:
            if self.df is None:
                self.featureEngineering()

            pipeline = self.preprocessing_pipeline()
            processed = pipeline.fit_transform(self.df)

            save_df(self.save_path)
            logger.info(f"Preprocessed data saved to {self.save_path}")

        except Exception as e:
            logger.error(f"Error in preprocessing: {e}")
            raise CustomError(e)
    

    


    
    
    
