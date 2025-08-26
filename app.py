from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/teamsquads", methods=["GET"])
def teamsquads():
    uid = request.args.get("uid")
    team = request.args.get("team")

    if not uid or not team:
        return jsonify({"error": "uid و team مطلوبين"}), 400

    try:
        # استدعاء ملف squad.py وتمرير uid + team
        output = subprocess.check_output(
            ["python3", "squad.py", uid, str(team)],
            text=True,
            stderr=subprocess.STDOUT
        )
        return jsonify({"success": True, "result": output})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": e.output}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# نقطة البداية في Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
