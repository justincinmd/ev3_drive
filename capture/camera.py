from picamera import PiCamera
import requests
from requests_futures.sessions import FuturesSession
import time
from io import BytesIO

print "Starting Camera"
camera = PiCamera()
camera.framerate = 30
camera.resolution = (160,120)
camera.start_preview()

print "Starting Capture"
session = FuturesSession()
stream = BytesIO()
last_response = None
last_second = 0
count = 0
for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
    stream.seek(0)
    count = count + 1
    if last_second != round(time.time()):
        last_second = round(time.time())
     	print "Frames per second: ", count   
        count = 0

    img_data = stream.read()
    stream.seek(0)
    stream.truncate()
    if last_response is not None:
        last_response.result()
    last_response = session.post('http://172.30.166.64:5000/', data=img_data)
