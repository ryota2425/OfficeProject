# coding: utf-8

#import文
import time
import picamera
import requests

#画像の撮影
def get_picture():

    with picamera.PiCamera() as camera:
        camera.resolution = (1920,1080)
        camera.start_preview()
        time.sleep(2)
        camera.capture('test.jpg')

#画像をサーバへ送信
def send_image_to_server():

    with open('test.jpg', mode = 'rb') as f:
        buf = f.read()
        print(len(buf))
    response = None
    files = {'image': ('test.jpg', buf, 'jpg/image')}
    response = requests.post('http://133.19.62.9:7070/upload_image', files=files)
    print(response)

def main():
    get_picture()
    send_image_to_server()

if __name__ == "__main__":
    main()

