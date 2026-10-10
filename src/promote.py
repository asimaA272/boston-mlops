"""Pre-prod / Prod ke liye: model re-log+register karna aur alias update karna."""
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
    # source alias wala model load -> naye run mein log -> naya version register -> new alias
    model = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@{a.source_alias}")
    mlflow.set_experiment(EXPERIMENT)
    with mlflow.start_run(run_name=f"promote-{a.new_alias}") as run:
        mlflow.set_tag("source_alias", a.source_alias)
        mlflow.sklearn.log_model(model, "model")
        mv = mlflow.register_model(f"runs:/{run.info.run_id}/model", MODEL_NAME)
    client.set_registered_model_alias(MODEL_NAME, a.new_alias, mv.version)
    print(f"{a.source_alias} -> registered version {mv.version} with alias '{a.new_alias}'")
else:
    mv = client.get_model_version_by_alias(MODEL_NAME, a.source_alias)
    client.set_registered_model_alias(MODEL_NAME, a.new_alias, mv.version)
    print(f"Version {mv.version}: alias '{a.new_alias}' laga diya")
