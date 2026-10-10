"""RF + Logistic Regression train, MLflow log, best ko register + alias Challenger."""
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from mlflow.tracking import MlflowClient
from common import EXPERIMENT, FEATURES, MODEL_NAME, TARGET

train = pd.read_csv("data/train.csv")
test = pd.read_csv("data/test.csv")
X_train, y_train = train[FEATURES], train[TARGET]
X_test, y_test = test[FEATURES], test[TARGET]

candidates = [
    ("random_forest",
     RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42),
     {"n_estimators": 200, "max_depth": 8}),
    ("logistic_regression",
     make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, C=1.0)),
     {"C": 1.0, "max_iter": 1000}),
]

mlflow.set_experiment(EXPERIMENT)
best = None
for name, model, params in candidates:
    with mlflow.start_run(run_name=name):
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        acc = accuracy_score(y_test, pred)
        f1 = f1_score(y_test, pred)
        mlflow.log_param("model_type", name)
        mlflow.log_params(params)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1", f1)
        info = mlflow.sklearn.log_model(model, name="model", serialization_format="cloudpickle")
        print(f"{name}: accuracy={acc:.4f} f1={f1:.4f}")
        if best is None or f1 > best["f1"]:
            best = {"name": name, "f1": f1, "uri": info.model_uri}

print("Best model:", best["name"])
mv = mlflow.register_model(best["uri"], MODEL_NAME)
client = MlflowClient()
client.set_registered_model_alias(MODEL_NAME, "Challenger", mv.version)
print(f"Registered {MODEL_NAME} version {mv.version} -> alias 'Challenger'")
