#!/bin/bash
echo -e "\n============================================="
echo -e "🔍  BOSTON MLOPS PIPELINE HEALTH CHECK RUN"
echo -e "=============================================\n"

# 1. Python Environment Check
echo -ne "1. Virtual Environment Status... "
if [ -d "venv" ]; then
    echo -e "✅ [OK] (venv folder exists)"
else
    echo -e "❌ [FAIL] (venv folder missing! Run 'python3 -m venv venv')"
fi

# 2. MLflow Central Server Verification
echo -ne "2. MLflow Local Logger (Port 5000)... "
if curl -s http://127.0.0 &>/dev/null || curl -s http://127.0.0 &>/dev/null; then
    echo -e "✅ [ACTIVE]"
else
    echo -e "❌ [DOWN] (MLflow server is closed! Run 'mlflow server --host 0.0.0.0 --port 5000')"
fi

# 3. Serving Containers Check
echo -ne "3. Sandbox Sandbox Serving (Port 5001)... "
if curl -s http://127.0.0 &>/dev/null; then echo -e "✅ [LIVE]"; else echo -e "⚪ [INACTIVE] (Waiting for Dev run)"; fi

echo -ne "4. Staging Environment Serving (Port 5002)... "
if curl -s http://127.0.0 &>/dev/null; then echo -e "✅ [LIVE]"; else echo -e "⚪ [INACTIVE] (Waiting for Pre-Prod merge)"; fi

echo -ne "5. Production Champion Serving (Port 5003)... "
if curl -s http://127.0.0 &>/dev/null; then echo -e "✅ [LIVE]"; else echo -e "⚪ [INACTIVE] (Waiting for Release Tag)"; fi

# 4. Source Data Integrity
echo -ne "6. Data Partition Splits Check... "
if [ -f "data/train.csv" ] && [ -f "data/test.csv" ]; then
    echo -e "✅ [OK] (Dataset splits exist)"
else
    echo -e "❌ [FAIL] (Data folder is empty! Run 'python3 src/ingest.py')"
fi

# 5. Local Git Synchronization status
echo -ne "7. Local Git Branch Tracking... "
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null)
if [ -n "$CURRENT_BRANCH" ]; then
    echo -e "✅ [OK] (Current active state: '$CURRENT_BRANCH')"
else
    echo -e "❌ [FAIL] (Not a valid Git folder)"
fi

echo -e "\n============================================="
