TIME=${1:-"5"} # 1ファイルあたりの録画時間


ffmpeg -i http://localhost:8080/?action=stream \
	-an -vcodec h264_omx \
	-f segment -segment_time $TIME \
	-segment_format_options movflags=+faststart -reset_timestamps 1 \
	-strftime 1 "/home/pi/traffic_test/video_src/video_data/%Y-%m-%d_%H-%M-%S.mp4"
