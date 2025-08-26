from flask import Flask, request, jsonify
from squad import FF_CLIENT, map_team_number  # فقط استورد FF_CLIENT و map_team_number

# تعريف الحساب هنا مباشرة
BOT_ACCOUNT_ID = "4130944097"
BOT_ACCOUNT_PASSWORD = "A25B68334573A33F8D85F4C5F9B974373C7C5424796448F535C121F5E56877A0"

app = Flask(__name__)

@app.route("/teamsquads", methods=["GET"])
def teamsquads():
    uid = request.args.get("uid")
    team = request.args.get("team")

    if not uid or not team:
        return jsonify({"error": "uid و team مطلوبين"}), 400

    try:
        team_number = map_team_number(int(team))
        client_thread = FF_CLIENT(
            id=BOT_ACCOUNT_ID,
            password=BOT_ACCOUNT_PASSWORD,
            target_uid=int(uid),
            team_number=team_number
        )
        client_thread.start()
        client_thread.join()
        return jsonify({"success": True, "result": f"تمت معالجة UID {uid} على Team {team}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
