#!/bin/bash

SERVER_IP="133.19.62.9"
COUNTER=0
DEVICE_ID=`cat /home/pi/office/id.conf`

COM2="bash /home/pi/office/office_stream.sh"

CMDNAME=`basename $0`
# 実行時に指定された引数の数が 1 でなければエラー終了。
if [ $# -ne 1 ]; then
  echo "Usage: $CMDNAME [--start or -s or --camera or --stop ]" 1>&2
  exit 1
fi

#プロセスを終了
if [ "$1" = '--stop' -o "$1" = '-t' ]; then
    pkill -e -f -9 "$COM2"
    pkill -e -f -9 "ffmpeg"
    exit 0
fi


#cameraのプロセスを実行
if [ "$1" = '--camera' -o "$1" = '--start' ]; then
    pkill -e -f -9 "$COM2"
    pkill -e -f -9 "ffmpeg"      # 一度終了処理を実行
    echo "ID = $DEVICE_ID"
    echo "`date '+%Y/%m/%d %H:%M:%S'` サーバへの接続確認開始"
    while [ "$COUNTER" -lt 1000 ]
    do
        ping "$SERVER_IP" -c 1 >> /dev/null
        if [ "$?" = "0" ]; then
            echo "`date '+%Y/%m/%d %H:%M:%S'` アクセス成功！"
            ${COM2} ${DEVICE_ID} >> /dev/null              
            exit 0
        else
            echo "`date '+%Y/%m/%d %H:%M:%S'` 5秒後に再試行します"
            sleep 5s
        fi
    let COUNTER++
    done
    echo "`date '+%Y/%m/%d %H:%M:%S'` 試行回数が上限に達したため終了します"
    exit 1
fi

#プロセスを終了
if [ "$1" = '--camerat' ]; then
    pkill -e -f -9 "$COM2"
    pkill -e -f -9 "ffmpeg"
    exit 0
fi

echo "`date '+%Y/%m/%d %H:%M:%S'` 引数エラー"

exit 0
