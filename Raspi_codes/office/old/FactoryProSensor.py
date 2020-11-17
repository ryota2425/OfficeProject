#!/usr/bin/env python3

import smbus
import math
from time import sleep
import time
import requests
import json
from datetime import datetime
import threading
import sys
from gpiozero import MCP3008
tmp = MCP3008(channel=0, device=0)

DEV_ADDR = 0x68

ACCEL_XOUT = 0x3b
ACCEL_YOUT = 0x3d
ACCEL_ZOUT = 0x3f
TEMP_OUT = 0x41
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47

PWR_MGMT_1 = 0x6b
PWR_MGMT_2 = 0x6c  

i2c_error = False

bus = smbus.SMBus(1)
try:
    bus.write_byte_data(DEV_ADDR, PWR_MGMT_1, 0)
except:
    print("i2c初期化エラーです。以後回復するまで0で処理されます。") 
    i2c_error = True

#データの格納用
MIMETYPE = 'application/json'
data_rec_int = 0.1
data_send_int = 5        #送信間隔（秒）
data_temp_max = 500     #バッファのサイズ
data_temp_array_max = 12   #バッファ数
data_temp = [str()] * data_temp_array_max  #バッファ
data_temp_array_index = 0   #今のバッファ番号
data_temp_index = 0         #バッファ内の位置
data_send_flag = [False] * data_temp_array_max  #どのバッファが送信待ちか
data_send_last = data_temp_array_max - 1    #前回送信済のバッファ番号
# デバイス情報
#version = "0.100"                     # バージョン
deviceid = 1                          # デバイスID

CONNECTION_RETRY = 4    #接続リトライ回数

factory_auth = ('factory', 'factorypass')

# デバイスID
args = sys.argv
if(len(args) == 2):
  deviceid = int(args[1])
else:
  deviceid = 1  
  print("IDが未指定です")                        
print("ID:" + str(deviceid))


def read_word(adr):
    high = bus.read_byte_data(DEV_ADDR, adr)
    low = bus.read_byte_data(DEV_ADDR, adr+1)
    val = (high << 8) + low
    return val

def read_word_sensor(adr):
    val = read_word(adr)
    if (val >= 0x8000):  
        return -((65535 - val) + 1)
    else:  
        return val

def get_temp():
    temp = read_word_sensor(TEMP_OUT)
    x = temp / 340 + 36.53      # data sheet(register map)記載の計算式.
    return x

def getGyro():
    x = read_word_sensor(GYRO_XOUT) / 131.0
    y = read_word_sensor(GYRO_YOUT) / 131.0
    z = read_word_sensor(GYRO_ZOUT) / 131.0
    return [x, y, z]


def getAccel():
    x = read_word_sensor(ACCEL_XOUT) / 16384.0
    y = read_word_sensor(ACCEL_YOUT) / 16384.0
    z = read_word_sensor(ACCEL_ZOUT) / 16384.0
    return [x, y, z]

def getCT():
    ct_value = tmp.value * 3.3
    return ct_value


def send_server():
    global data_send_last, data_temp, data_temp_array_index, data_temp_index, data_send_flag
    send_target_index = 0 #次に出力するバッファ番号
    while True:
        if(data_send_last < data_temp_array_max-1): #バッファ番号が末尾まできたら0に
            send_target_index = data_send_last + 1
        else :
            send_target_index = 0
    
        if(data_send_flag[send_target_index] == True):  #対象のバッファの送信要求がTrueだったら
        
            #サーバへの送信（リトライ処理付き）
            response = None
            sendsucess=False
            #url = 'http://133.19.62.7:18567'
            url = 'http://133.19.62.9:3000/api/v1/upload_data/sensor'
            headers = {'content-type': 'application/json'}
            
            data_temp[send_target_index] = data_temp[send_target_index].rstrip(",\n")
            send_data = '{"datas": [' + data_temp[send_target_index] + ']}'
            #print(send_data)
            for i in range(1, CONNECTION_RETRY + 1):
                try:
                    response = requests.post(url, data=send_data, headers=headers, auth=factory_auth)
                except Exception as e:
                    print("サーバ送信エラー！  retry:{i}/{max} wait:{w}s".format( i=i, max=CONNECTION_RETRY, w=i * 2))
                    if(data_send_flag.count(True) >= (data_temp_array_max-3)):
                        print("バッファが残り少ないのでリトライを中断します")
                        break
                    time.sleep(i * 2)
                else:
                    sendsucess=True
                    print("SEND_SUCESS[" + str(response.status_code) +  \
                        "]: バッファ番号[" + str(send_target_index) + "]")
                    break

            if(not sendsucess):
                print("送信失敗、データは破棄されます")

            data_send_flag[send_target_index] = False # 送信要求をFalseに戻す
            data_send_last = send_target_index        # バッファ番号を次に        

        time.sleep(0.5)


def main_getSensors():
    global data_temp, data_temp_array_index, data_temp_index, data_send_flag, i2c_error
    sendlasttime = time.time()
    time_temp = 0

    while True:
        nowTime = time.time()
        if(nowTime - time_temp >= data_rec_int):
            if(not i2c_error):
                try:
                    ax, ay, az = getAccel()
                    gx, gy, gz = getGyro()
                    temp = get_temp()
                except:
                    print("i2c読み取りエラーです。以後回復するまで0で処理されます。")
                    ax, ay, az = 0, 0, 0
                    gx, gy, gz = 0, 0, 0
                    temp = 0
                    i2c_error = True
            else:
                try:
                    bus.write_byte_data(DEV_ADDR, PWR_MGMT_1, 0)
                    ax, ay, az = getAccel()
                    gx, gy, gz = getGyro()
                    temp = get_temp()
                    print("i2cのエラーから回復しました")
                    i2c_error = False
                except:
                    ax, ay, az = 0, 0, 0
                    gx, gy, gz = 0, 0, 0
                    temp = 0

            ct = getCT()

            json_data = {'machine_id':deviceid, 'datetime':int(nowTime*1000), 'Accel':{'x':ax, 'y':ay, 'z':az}, 'Gyro':{'x':gx, 'y':gy, 'z':gz}, 'temp':temp, 'mcp':ct}
            data_temp[data_temp_array_index] += json.dumps(json_data) + ",\n" 

            data_temp_index += 1    #バッファ内のインデックスを次へ
            time_temp = time.time()
            if(data_temp_index >= data_temp_max or \
                time_temp - sendlasttime >=  data_send_int): #現在のバッファが一杯になったとき or 一定時間経過
                #デバッグ用
                print("バッファ[" + str(data_temp_array_index) + "]：" \
                    + str(data_temp_index) + "個, " + str(time_temp - sendlasttime) + "秒")
                sendlasttime = time_temp

                data_send_flag[data_temp_array_index] = True  #送信要求をTrueに
                data_temp_index = 0                 #バッファ内インデックスを初期化
                data_temp_array_index += 1          #バッファ番号を次へ
                if(data_temp_array_index >= data_temp_array_max): #最後のバッファに到達した場合
                    data_temp_array_index = 0                       #最初に戻る
                data_temp[data_temp_array_index] = str()
                    
                if(data_send_flag[data_temp_array_index] == True):  #未送信のバッファに追いついた場合エラーで終了
                    print('Error: The data list waiting to be sent has exceeded the limit', file=sys.stderr)
                    sys.exit()



if __name__ == '__main__':
    sendthread = threading.Thread(target=send_server, daemon=True)
    sendthread.start()
    main_getSensors()