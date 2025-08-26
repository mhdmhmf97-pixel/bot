from flask import Flask, request, jsonify
import subprocess
import sys
import os

app = Flask(__name__)

@app.route("/api/teamsquads", methods=["GET"])
def teamsquads_api():
    uid = request.args.get("uid")
    team = request.args.get("team")
    
    if not uid or not team:
        return jsonify({"error": "Missing uid or team"}), 400

    try:
        # استدعاء سكواد كبروسيس خارجي
        result = subprocess.run(
            [sys.executable, "squad.py", uid, team],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        return jsonify({"status": "success", "output": output})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "error": e.stderr.strip()})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
