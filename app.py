from flask import Flask, request, jsonify
from squad import FF_CLIENT, map_team_number  # استيراد الكلاس والدالة من squad.py
import threading

app = Flask(__name__)

# لتخزين كل العمليات الجارية (اختياري)
active_clients = []

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
        # إنشاء Thread لتشغيل FF_CLIENT
        client_thread = FF_CLIENT(
            id="4130944097",  # ضع حسابك هنا
            password="A25B68334573A33F8D85F4C5F9B974373C7C5424796448F535C121F5E56877A0"
            target_uid=uid,
            team_number=team_number
        )
        client_thread.start()
        active_clients.append(client_thread)  # حفظ الـ Thread إذا أردنا متابعته لاحقًا

        return jsonify({
            "success": True,
            "msg": f"تم إرسال UID={uid} إلى Team {team_number}"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
