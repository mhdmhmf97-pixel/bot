import subprocess
import sys
import os

# -------------------------
# تثبيت المكتبات تلقائيًا إذا لم تكن موجودة
required_packages = [
    "pyjwt", "requests", "protobuf", "psutil", "protobuf-decoder",
    "pycryptodome", "httpx", "urllib3", "flask"
]

for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# -------------------------
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

def run_squad(uid, team):
    """
    تشغيل سكربت squad.py مع UID و team
    """
    try:
        script_path = os.path.join(os.path.dirname(__file__), "squad.py")
        if not os.path.exists(script_path):
            return None, f"squad.py not found at {script_path}"

        result = subprocess.run(
            [sys.executable, script_path, str(uid), str(team)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=180  # وقت أطول لتجنب توقف السكربت
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return None, "Timeout expired while running squad.py"
    except Exception as e:
        return None, str(e)

@app.route("/api/teamsquads", methods=["GET"])
def teamsquad_api():
    uid = request.args.get("uid")
    team = request.args.get("team")

    if not uid or not team:
        return jsonify({"status": "error", "message": "uid and team parameters are required"}), 400

    try:
        uid = int(uid)
        team = int(team)
    except ValueError:
        return jsonify({"status": "error", "message": "uid and team must be integers"}), 400

    print(f"[DEBUG] Running squad.py with UID: {uid}, Team: {team}")

    stdout, stderr = run_squad(uid, team)

    if stderr:
        return jsonify({"status": "error", "message": stderr, "output": stdout}), 500

    return jsonify({"status": "success", "output": stdout})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
