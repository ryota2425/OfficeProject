MACHINE_ID=$1

ffmpeg -f alsa -thread_queue_size 1024 -v error \
  -f v4l2 -thread_queue_size 512 -input_format yuyv422 -video_size 1280x720 \
  -i /dev/video0 \
  -filter_complex scale=1280x720,fps=20 \
  -c:v h264_omx -b:v 764k -g 24 \
  -c:a aac -b:a 64k \
  -flags +cgop+global_header \
  -f flv rtmp://133.19.62.9:10500/live/${MACHINE_ID}
