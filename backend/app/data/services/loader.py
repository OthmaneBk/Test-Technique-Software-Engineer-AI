import os
from pathlib import Path

import pandas as pd


class DatasetLoader:
    DEFAULT_PATH = Path(__file__).resolve().parents[1] / "storage" / "data.csv"

    def __init__(self):
        self.path = self.DEFAULT_PATH

    def load(self) -> pd.DataFrame:
        if not os.path.isfile(self.path):
            raise FileNotFoundError(
                f"Dataset introuvable à {self.path}. "
            )

        df = pd.read_csv(self.path)

        return df
