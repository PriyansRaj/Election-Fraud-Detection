from src.error import CustomError
from src.logging import logger
def read_csv(csv_path: str) -> pd.DataFrame:
   
    logger.info(f"Reading CSV file from path: {csv_path}")
    try:
        df = pd.read_csv(csv_path)
        logger.info(f"CSV loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error while reading CSV: {e}")
        raise CustomError(e, sys)

def save_df(df: pd.DataFrame, save_path: str):
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False)
        logger.info(f"File saved successfully: {save_path}")
    except Exception as e:
        logger.error(f"Failed to save file at {save_path}: {e}")
        raise CustomError(e, sys)