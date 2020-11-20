from flask import Flask, request, render_template, jsonify
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.after_request
def afterRequest(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response



# 現在のFPS, 録画時間を取得
@app.route('/get_current_params')
def getCurrentParams():
    # TODO: DB読み取り処理やエラー用処理を記述
    # ここから

    # ここまで

    return jsonify({'fps': 30, 'recordingTime': 5})


# FPSを変更
@app.route('/set_fps', methods=['POST'])
def setFps():
    data = json.loads(request.get_data().decode())
    fps = int(data['fps'])
    print('Set FPS:', fps)

    # TODO: DB更新処理やエラー用処理を記述
    # ここから

    # ここまで

    return jsonify({'result': 'OK'})


# 録画時間を変更
@app.route('/set_recordingTime', methods=['POST'])
def setRecordingTime():
    data = json.loads(request.get_data().decode())
    recordingTime = int(data['recordingTime'])
    print('Set Recording Time:', recordingTime)

    # TODO: DB更新処理やエラー用処理を記述
    # ここから

    # ここまで

    return jsonify({'result': 'OK'})


def main():
    app.run(host='0.0.0.0', port=60080)


if __name__ == '__main__':
    main()
