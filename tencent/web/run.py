from flask import Flask, request, make_response, jsonify
import settings_flask

flask_app = Flask(__name__)

flask_app.config.from_object(settings_flask)

g_data={}
g_data["nbzth"] = {}
# g_data ={}

@flask_app.route('/api/miniprogram/nbcb/nbzth', methods=["POST"])
def get_hello_world():
    data = request.json
    g_data["nbzth"] = data
    print(g_data["nbzth"])
    return make_response(jsonify({'code': 200, "msg": "更改成功", "data": {}}), 200)


@flask_app.route('/api/miniprogram/nbcb/nbzth', methods=["GET"])
def set_hello_world():
    print(g_data["nbzth"])
    return make_response(jsonify({'code': 200, "msg": "获取成功", "data": g_data.get("nbzth", {})}), 200)


if __name__ == '__main__':
    flask_app.run(debug=False)
