from flask import Flask, request, jsonify
import threading
import logging
from squad import FF_CLIENT, BOT_ACCOUNT_ID, BOT_ACCOUNT_PASSWORD, map_team_number

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

def run_client(uid, team_input, result_dict):
    try:
        team_number = map_team_number(int(team_input))
        logging.info(f"Preparing to invite UID {uid} to Team {team_number}")
        
        client_thread = FF_CLIENT(
            id=BOT_ACCOUNT_ID,
            password=BOT_ACCOUNT_PASSWORD,
            target_uid=int(uid),
            team_number=team_number
        )

        # تسجيل الأحداث من FF_CLIENT
        original_info = logging.getLogger().info
        def capture_log(msg, *args, **kwargs):
            if 'logs' not in result_dict:
                result_dict['logs'] = []
            result_dict['logs'].append(str(msg))
            original_info(msg, *args, **kwargs)
        logging.getLogger().info = capture_log

        client_thread.start()
        client_thread.join()
        result_dict['success'] = True
        result_dict['message'] = f"UID {uid} has been invited to Team {team_input}"
    except Exception as e:
        result_dict['success'] = False
        result_dict['message'] = str(e)

@app.route("/teamsquads", methods=["GET"])
def teamsquads():
    uid = request.args.get("uid")
    team = request.args.get("team")

    if not uid or not team:
        return jsonify({"error": "uid و team مطلوبين"}), 400

    result_dict = {}
    thread = threading.Thread(target=run_client, args=(uid, team, result_dict))
    thread.start()
    thread.join()  # ننتظر انتهاء العملية قبل الرد

    return jsonify(result_dict)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
