from flask import Flask, request, jsonify
import traceback
from squad import FF_CLIENT, map_team_number

# ضع حساب البوت هنا
BOT_ACCOUNT_ID = "3972631254"
BOT_ACCOUNT_PASSWORD = "654BF523ECA7CBA017304C1FD5AFC69F65DE6742FF5415FCADD12C8B6BE8A042"

app = Flask(__name__)

@app.route("/teamsquads", methods=["GET"])
def teamsquads():
    uid = request.args.get("uid")
    team_input = request.args.get("team")

    if not uid or not team_input:
        return jsonify({"error": "uid و team مطلوبين"}), 400

    try:
        uid = int(uid)
        team_input = int(team_input)
        if team_input not in [3,4,5,6]:
            return jsonify({"error": "team يجب أن يكون 3، 4، 5 أو 6"}), 400

        team_number = map_team_number(team_input)

        client = FF_CLIENT(
            id=4130944097,
            password=A25B68334573A33F8D85F4C5F9B974373C7C5424796448F535C121F5E56877A0,
            target_uid=uid,
            team_number=team_number
        )

        # تشغيل البوت وانتظار انتهاء التنفيذ
        client.start()
        client.join()

        return jsonify({
            "success": True,
            "msg": f"تم إرسال UID={uid} إلى Team {team_number} بنجاح"
        })

    except Exception as e:
        traceback_str = traceback.format_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback_str
        }), 500

if __name__ == "__main__":
    # على Render أو محلي
    app.run(host="0.0.0.0", port=10000)
