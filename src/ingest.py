"""Step 1: Boston dataset load -> classification label banao -> train/test split."""
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from common import FEATURES, TARGET

RAW = "data/boston_raw.csv"


def download_boston():
    try:
        from sklearn.datasets import fetch_openml
        df = fetch_openml(name="boston", version=1, as_frame=True, parser="auto").frame
        df = df.apply(lambda c: pd.to_numeric(c.astype(str)))
        print("Dataset OpenML se aaya")
        return df
    except Exception as e:
        print("OpenML fail:", e, "-> CMU se try kar raha hoon")
    url = "http://lib.stat.cmu.edu/datasets/boston"
    raw = pd.read_csv(url, sep=r"\s+", skiprows=22, header=None)
    data = np.hstack([raw.values[::2, :], raw.values[1::2, :2]])
    target = raw.values[1::2, 2]
    df = pd.DataFrame(data, columns=FEATURES)
    df["MEDV"] = target
    return df


def main():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(RAW):
        df = pd.read_csv(RAW)
    else:
        df = download_boston()
        df.to_csv(RAW, index=False)
    df = df.dropna()
    # Regression -> Classification (Logistic Regression ke liye zaroori)
    df[TARGET] = (df["MEDV"] > df["MEDV"].median()).astype(int)
    df = df.drop(columns=["MEDV"])      # leakage rokne ke liye
    train, test = train_test_split(df, test_size=0.2, random_state=42, stratify=df[TARGET])
    train.to_csv("data/train.csv", index=False)
    test.to_csv("data/test.csv", index=False)
    print(f"Ingest done. train={len(train)} test={len(test)}")


if __name__ == "__main__":
    main()
