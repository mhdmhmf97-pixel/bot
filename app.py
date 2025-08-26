from flask import Flask, request, jsonify
from squad import FF_CLIENT, map_team_number  # استدعاء البوت بالكامل من squad.py

app = Flask(__name__)

# ضع بيانات الحساب الذي سيستخدم للاتصال باللعبة
BOT_ACCOUNT_ID = "3972631254"
BOT_ACCOUNT_PASSWORD = "كلمة_مرور_الحساب_هنا"

@app.route("/teamsquads", methods=["GET"])
def teamsquads():
    uid = request.args.get("uid")
    team_input = request.args.get("team")

    if not uid or not team_input:
        return jsonify({"error": "uid و team مطلوبين"}), 400

    try:
        uid = int(uid)
        team_input = int(team_input)
        team_number = map_team_number(team_input)
    except ValueError:
        return jsonify({"error": "uid و team يجب أن يكونا أرقام"}), 400

    try:
        # إنشاء وتشغيل FF_CLIENT من squad.py مباشرة
        client = FF_CLIENT(
            id=4130944097,
            password=A25B68334573A33F8D85F4C5F9B974373C7C5424796448F535C121F5E56877A0,
            target_uid=uid,
            team_number=team_number
        )
        client.start()
        client.join()  # انتظر حتى ينتهي البوت من كل العملية

        return jsonify({
            "success": True,
            "msg": f"تم إرسال UID={uid} إلى Team {team_number} بنجاح"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
