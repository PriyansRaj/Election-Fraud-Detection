import pandas as pd
import numpy as np
import os
import sys
from src.error import CustomError
from src.logging import logger
from src.utils import read_csv



class FeatureEngineering:
   

    def __init__(self, csv_path: str = ""):
        self.csv_path = csv_path
        self.save_path = os.path.join("artifacts", "engineered.csv")
        self.df = read_csv(csv_path)

   

    def voter_turnout(self) -> None:
      
        try:
            self.df["voter_turnout"] = (self.df["totvotpoll"] / self.df["electors"]) * 100
            logger.info("Voter turnout calculated successfully")
        except KeyError as e:
            logger.error("Missing columns for voter turnout calculation")
            raise CustomError(e, sys)
        except Exception as e:
            logger.error(f"Unexpected error in voter_turnout: {e}")
            raise CustomError(e, sys)

    def vote_share(self) -> None:
        
        required_cols = ["year", "pc_name", "totvotpoll"]
        try:
            if not all(col in self.df.columns for col in required_cols):
                raise KeyError(f"Missing one of required columns: {required_cols}")

            self.df["vote_share"] = (
                self.df.groupby(["year", "pc_name"])["totvotpoll"]
                .transform(lambda x: (x / x.sum()) * 100)
            )
            logger.info("Vote share calculated successfully")
        except Exception as e:
            logger.error(f"Error calculating vote share: {e}")
            raise CustomError(e, sys)

    @staticmethod
    def calc_pdi(group: pd.DataFrame) -> float:
        shares = group["vote_share"] / 100
        return (shares ** 2).sum()

    def get_pdi(self) -> None:
        try:
            if "vote_share" not in self.df.columns:
                raise ValueError("Run vote_share() before get_pdi().")

            party_votes = (
                self.df.groupby(["year", "st_name", "partyname"])["vote_share"]
                .mean()
                .reset_index()
            )
            pdi = (
                party_votes.groupby(["year", "st_name"])
                .apply(self.calc_pdi)
                .reset_index(name="pdi")
            )
            self.df = self.df.merge(pdi, on=["year", "st_name"], how="left")
            logger.info("PDI calculated and merged successfully")
        except Exception as e:
            logger.error(f"Error in get_pdi: {e}")
            raise CustomError(e, sys)


    def save(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            self.df.to_csv(self.save_path, index=False)
            logger.info(f"Processed data saved to {self.save_path}")
        except Exception as e:
            logger.error(f"Error saving processed data: {e}")
            raise CustomError(e, sys)

