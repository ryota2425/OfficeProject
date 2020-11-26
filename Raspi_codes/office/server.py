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
    try:
        # ローカルJSONファイルの読み書き
        with open('setting.json', 'r') as f:
            setting = json.load(f)
            fps = setting["fps"] 
            #秒=>分への変換
            recordingTime = setting["recordingTime"] 
            resolution = setting["resolution"] 
            
    except Exception as e:
        #エラーハンドリング
        print(e)
        return jsonify({'result': 'NG'})
    else:
        #成功した時の処理
        print('Setting Parameters:', setting)
        response = setting
        response["result"] = "OK"
        print(response) 
    # ここまで

    # エラーのときは、return jsonify({'result': 'NG'})
    return jsonify(response)


# FPSを変更
@app.route('/set_fps', methods=['POST'])
def setFps():
    data = json.loads(request.get_data().decode())
    fps = int(data['fps'])
    #JSONファイルを更新する
    try:
        # ローカルJSONファイルの読み書き
        with open('setting.json', 'r') as f:
            setting = json.load(f)
            setting["fps"] = fps
        with open('setting.json', 'w') as f:
            f.write(json.dumps(setting))   
    except Exception as e:
        #エラーハンドリング
        print(e)
        return jsonify({'result': 'NG'})
    else:
        #成功した時の処理
        print('Set FPS:', fps)
        print(data)
    # TODO: DB更新処理やエラー用処理を記述
    # ここから

    # ここまで

    # エラーのときは、return jsonify({'result': 'NG'})
    return jsonify({'result': 'OK'})


# 録画時間を変更
@app.route('/set_recordingTime', methods=['POST'])
def setRecordingTime():
    data = json.loads(request.get_data().decode())
    recordingTime = int(data['recordingTime'])
    print('Set Recording Time:', recordingTime)

    #JSONファイルを更新する
    try:
        # ローカルJSONファイルの読み書き
        with open('setting.json', 'r') as f:
            setting = json.load(f)
            setting["recordingTime"] = recordingTime
        with open('setting.json', 'w') as f:
            f.write(json.dumps(setting))
    except Exception as e:
        #エラーハンドリング
        print(e)
        return jsonify({'result': 'NG'})
    else:
        #成功した時の処理
        print('Set recordingTime:', recordingTime)
        print(data)

    # TODO: DB更新処理やエラー用処理を記述
    # ここから

    # ここまで

    # エラーのときは、return jsonify({'result': 'NG'})
    return jsonify({'result': 'OK'})


# 解像度を変更
@app.route('/set_resolution', methods=['POST'])
def setResolution():
    data = json.loads(request.get_data().decode())
    resolution = int(data['resolution'])
    print('Set resolution:', resolution)

    #JSONファイルを更新する
    try:
        # ローカルJSONファイルの読み書き
        with open('setting.json', 'r') as f:
            setting = json.load(f)
            setting["resolution"] = resolution
        with open('setting.json', 'w') as f:
            f.write(json.dumps(setting))
    except Exception as e:
        #エラーハンドリング
        print(e)
        return jsonify({'result': 'NG'})
    else:
        #成功した時の処理
        print('Set resolution:', resolution)
        print(data)


    # TODO: DB更新処理やエラー用処理を記述
    # ここから

    # ここまで

    # エラーのときは、return jsonify({'result': 'NG'})
    return jsonify({'result': 'OK'})


def main():
    app.run(host='0.0.0.0', port=60080)


if __name__ == '__main__':
    main()
