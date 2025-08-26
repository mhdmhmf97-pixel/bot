from flask import Flask, request, jsonify
import subprocess
import sys
import threading

app = Flask(__name__)

def run_squad(uid, team):
    try:
        # استدعاء سكربت squad.py مع uid و team
        result = subprocess.run(
            [sys.executable, "squad.py", str(uid), str(team)],
            capture_output=True,
            text=True,
            timeout=60  # لتجنب توقف العملية للأبد
        )
        return result.stdout, result.stderr
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

    stdout, stderr = run_squad(uid, team)

    if stderr:
        return jsonify({"status": "error", "message": stderr}), 500

    return jsonify({"status": "success", "output": stdout})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
