"""Model Test: alias wala model load karo, test data par check karo."""
import argparse
import sys
import mlflow.sklearn
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from common import FEATURES, MIN_ACCURACY, MODEL_NAME, TARGET

p = argparse.ArgumentParser()
p.add_argument("--alias", required=True)
a = p.parse_args()

model = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@{a.alias}")
test = pd.read_csv("data/test.csv")
pred = model.predict(test[FEATURES])
acc = accuracy_score(test[TARGET], pred)
f1 = f1_score(test[TARGET], pred)
print(f"[{a.alias}] accuracy={acc:.4f} f1={f1:.4f} (minimum {MIN_ACCURACY})")
if acc < MIN_ACCURACY:
    print("MODEL TEST FAILED")
    sys.exit(1)
print("MODEL TEST PASSED")
