from time import sleep
from picamera import PiCamera
from ocr import Converter

def shoot_one():
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture('img/img.jpg')

if __name__ == '__main__':
    while True:
       img = Converter.from_cam(save_path='img/cam_tmp.jpg')
       img.preproc()
       img.to_text()
       img.classify()
       print(img.rslt)
       img.save_db()
       sleep(30)

