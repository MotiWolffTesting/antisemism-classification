import pandas as pd


class DataLoader:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data = None
        self.load_data()
        
    def load_data(self) -> None:
        "Load dataset from csv file"
        try:
            self.data = pd.read_csv(self.data_path)
            print(f"Dataset loaded successfully! Shape is: {self.data.shape}")
        except Exception as e:
            print(f"Error loading dataset: {e}")
            raise