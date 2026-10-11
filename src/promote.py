"""Pre-prod / Prod: model re-log+register aur alias update."""
import argparse
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from common import EXPERIMENT, MODEL_NAME

p = argparse.ArgumentParser()
p.add_argument("action", choices=["register", "alias"])
p.add_argument("--source-alias", required=True)
p.add_argument("--new-alias", required=True)
a = p.parse_args()
client = MlflowClient()

if a.action == "register":
    # 1. Purana model load karein
    model = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@{a.source_alias}")
    mlflow.set_experiment(EXPERIMENT)
    
    # 2. Naye run mein log karein (Fixed parameter here)
    with mlflow.start_run(run_name=f"promote-{a.new_alias}"):
        mlflow.set_tag("source_alias", a.source_alias)
        info = mlflow.sklearn.log_model(model, "model", serialization_format="cloudpickle")
        mv = mlflow.register_model(info.model_uri, MODEL_NAME)
        
    # 3. Naya alias set karein
    client.set_registered_model_alias(MODEL_NAME, a.new_alias, mv.version)
    print(f"{a.source_alias} -> version {mv.version} with alias '{a.new_alias}'")
else:
    # Direct alias update bina kisi delay ya re-logging ke
    mv = client.get_model_version_by_alias(MODEL_NAME, a.source_alias)
    client.set_registered_model_alias(MODEL_NAME, a.new_alias, mv.version)
    print(f"Version {mv.version}: alias '{a.new_alias}' laga diya")

