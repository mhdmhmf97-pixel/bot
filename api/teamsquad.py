from flask import Flask, request, jsonify
import subprocess
import sys
import os

app = Flask(__name__)

@app.route("/teamsquads", methods=["GET"])
def teamsquads():
    uid = request.args.get("uid")
    team = request.args.get("team")

    if not uid or not team:
        return jsonify({"error": "uid و team مطلوبين"}), 400

    python_executable = sys.executable
    squad_path = os.path.join(os.path.dirname(__file__), "../squad.py")

    try:
        output = subprocess.check_output(
            [python_executable, squad_path, str(uid), str(team)],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=120
        )
        return jsonify({"success": True, "result": output})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": e.output}), 500
    except subprocess.TimeoutExpired:
        return jsonify({"success": False, "error": "Timeout"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
