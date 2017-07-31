from db import LiteDB
from picamera import PiCamera
from PIL import Image, ImageFilter
from time import sleep
from datetime import datetime
import pytesseract
import sqlite3
import io

class Converter(object):
    def __init__(self, image=None):
        self.img = image
        self.txt = None
        self.rslt = None
    @classmethod
    def from_cam(cls, save_path):
        strm = io.BytesIO()
        with PiCamera() as cam:
            cam.resolution = (1024, 768)
            cam.start_preview()
            sleep(2) # Camera warm-up time
            cam.capture(strm, format='jpeg')
        strm.seek(0)
        img = Image.open(strm)
        img.save(save_path, 'JPEG')
        return cls(image=img)    
    @classmethod
    def from_path(cls, open_path):
        img = Image.open(open_path, 'r')
        return cls(image=img)
    def preproc(self, thres=200, mfsize=3):
        img = self.img
        # grayscale
        img = img.convert('L')
        # basic threshold
        img = img.point(lambda p: p > thres and 255)
        # basic blurring
        img = img.filter(ImageFilter.MedianFilter(size=mfsize))
        self.img = img        
    def resize(self):
        img = self.img
        size = 1600, 1600
        img.thumbnail(size)
        self.img = img
    def save_img(self, fpath):
        self.img.save(fpath, 'JPEG')
    def to_text(self):
        self.txt = pytesseract.image_to_string(self.img)
    def classify(self):
        r = 'unsure'
        words = self.txt.split()
        words = [w.lower() for w in words]
        good = ['what', 'like', 'today', 'coffee', 'chocolate']
        if any(w in words for w in good):
            r = 'good'
        else:
            r = 'bad'
        self.rslt = r
        return r
    def available(self):
        # TODO
        # check which options are available
        pass      
    def save_db(self):
        ldb = LiteDB()
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ldb.post(ts=ts, st=self.rslt)
 
