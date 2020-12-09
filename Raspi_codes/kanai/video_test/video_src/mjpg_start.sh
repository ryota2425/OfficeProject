#!/bin/sh

PORT="8080" #ポート番号
ID="kanai" #ID
PW="kanaipass" #パスワード

FRAMERATE=${1:-"30"} # FPS
SIZE=${2:-"640x480"} #解像度

export LD_LIBRARY_PATH=/usr/local/lib

#./mjpg_streamer \
 #   -i "input_uvc.so -f $FRAMERATE -r $SIZE -d /dev/video1 -y -n" \
  #  -o "output_http.so -w /usr/local/www -p $PORT -c $ID:$PW"
/home/pi/mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer \
    -i "/home/pi/mjpg-streamer/mjpg-streamer-experimental/input_uvc.so -f $FRAMERATE -r $SIZE -d /dev/video0 -y -n" \
    -o "/home/pi/mjpg-streamer/mjpg-streamer-experimental/output_http.so -w /usr/local/www -p $PORT"
