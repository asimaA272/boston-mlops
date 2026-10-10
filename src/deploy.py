"""Model Deploy: mlflow models serve se alias wala model port par chalao."""
import argparse
import json
import os
import signal
import subprocess
import sys
import time
import urllib.request
import pandas as pd
from common import FEATURES, MODEL_NAME, TRACKING_URI

p = argparse.ArgumentParser()
p.add_argument("--alias", required=True)
p.add_argument("--port", type=int, required=True)
a = p.parse_args()

pid_file = f".deploy_{a.port}.pid"
if os.path.exists(pid_file):                      # purana server band karo
    try:
        os.killpg(int(open(pid_file).read()), signal.SIGTERM)
        time.sleep(2)
    except Exception:
        pass

env = dict(os.environ, MLFLOW_TRACKING_URI=TRACKING_URI,
           BUILD_ID="dontKillMe", JENKINS_NODE_COOKIE="dontKillMe")
cmd = [sys.executable, "-m", "mlflow", "models", "serve",
       "-m", f"models:/{MODEL_NAME}@{a.alias}",
       "-p", str(a.port), "-h", "0.0.0.0", "--env-manager", "local"]
log = open(f"serve_{a.port}.log", "w")
proc = subprocess.Popen(cmd, env=env, stdout=log, stderr=log, start_new_session=True)
open(pid_file, "w").write(str(proc.pid))

base = f"http://127.0.0.1:{a.port}"
for _ in range(60):                               # max ~2 minute wait
    try:
        urllib.request.urlopen(base + "/ping", timeout=2)
        break
    except Exception:
        time.sleep(2)
else:
    print("Server start nahi hua, serve log dekho")
    sys.exit(1)

row = pd.read_csv("data/test.csv")[FEATURES].iloc[[0]]
payload = json.dumps({"dataframe_split": {"columns": FEATURES, "data": row.values.tolist()}})
req = urllib.request.Request(base + "/invocations", payload.encode(),
                             {"Content-Type": "application/json"})
print("Smoke test prediction:", urllib.request.urlopen(req, timeout=10).read().decode())
print(f"Deployed '{a.alias}' on {base}")
