# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import io
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 24
rawCapture = PiRGBArray(camera, size=(320, 240))
# allow the camera to warmup
time.sleep(0.1)


image_list = []

raw_input("Press any key to start recording 60 second video...")
# capture frames from the camera
start = time.time()
stream = io.BytesIO()
for frame in camera.capture_continuous(stream , format='jpeg', use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image_list.append(frame.getvalue())
        stream.truncate()
        stream.seek(0)
 
	# show the frame
	if(time.time() - start > 60):
		break
 
raw_input("Press any key to write JPG images...")

i = 0;
for img in image_list:
	out_str = "output/" + str(i) + ".jpg"
	with open(out_str, 'wb') as f:
		f.write(img)
	i+=1
