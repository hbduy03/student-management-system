import joblib
import numpy as np
from pathlib import Path

class StudentStatusModel:
    def __init__(self, model_path: str):
        p = Path(model_path)
        if not p.exists():
            raise FileNotFoundError(f"Model file not found: {p}")
        self.model = joblib.load(p)

    def predict_proba(self, midterm: float, ) -> float:
        X = np.array([[midterm,]], dtype=float)
        return float(self.model.predict_proba(X)[0, 1])

    def predict_status(self, midterm: float, threshold: float = 0.5) -> int:
        return int(self.predict_proba(midterm) >= threshold)
