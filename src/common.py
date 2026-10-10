import os
import mlflow

TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
mlflow.set_tracking_uri(TRACKING_URI)

MODEL_NAME = "boston_house_classifier"
EXPERIMENT = "boston-house-mlops"
FEATURES = ["CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE",
            "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"]
TARGET = "PRICE_HIGH"      # 1 = ghar mehnga (price median se upar), 0 = sasta
MIN_ACCURACY = 0.80        # isse kam ho to Model Test FAIL
