import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.download_cuad import download_cuad_dataset, CUAD_JSON_PATH
from modules.cuad_preprocessor import prepare_training_data


def run_cuad_pipeline():
    """
    Downloads CUAD dataset, loads annotations, pre-processes training data,
    and generates train/test split CSV files in the data directory.
    """
    print("--- Step 1: Downloading CUAD Dataset ---")
    json_path = download_cuad_dataset(CUAD_JSON_PATH)
    
    print("\n--- Step 2: Processing Annotations & Generating Train/Test Split ---")
    data_dir = os.path.dirname(json_path)
    train_df, test_df = prepare_training_data(json_path, data_dir=data_dir)
    
    print("\n--- Pipeline Completed ---")
    print(f"Train Dataset ({len(train_df)} rows) -> data/train.csv")
    print(f"Test Dataset  ({len(test_df)} rows)  -> data/test.csv")

if __name__ == "__main__":
    run_cuad_pipeline()
