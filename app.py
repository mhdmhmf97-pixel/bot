from flask import Flask, request, jsonify
import subprocess
import threading

app = Flask(__name__)

def run_squad(uid, team):
    """
    دالة تشغل squad.py في Thread لتجنب توقف Flask
    """
    def target():
        try:
            output = subprocess.check_output(
                ["python3", "squad.py", str(uid), str(team)],
                text=True,
                stderr=subprocess.STDOUT
            )
            print(f"Output squad.py: {output}")
        except subprocess.CalledProcessError as e:
            print(f"Error squad.py: {e.output}")
        except Exception as e:
            print(f"Exception squad.py: {e}")

    thread = threading.Thread(target=target)
    thread.start()


@app.route("/teamsquads", methods=["GET"])
def teamsquads():
    uid = request.args.get("uid")
    team = request.args.get("team")

    if not uid or not team:
        return jsonify({"error": "uid و team مطلوبين"}), 400

    run_squad(uid, team)
    return jsonify({"success": True, "msg": f"تم استقبال UID={uid} و Team={team}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
