import pandas as pd 
import numpy as np 
from sklearn.preprocessing import OneHotEncoder, LabelEncoder,OrdinalEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from src.feature_engineering import FeatureEngineering
from src.utils import read_csv

class DataPreprocessing:
    def __init__(self,csv_path):
        self.csv_path = csv_path
        self.df = read_csv(csv_path=csv_path)
        self.save_path = os.path.join("artifacts", "preprocessed.csv")
    
