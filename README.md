# Butler
Silly little flask app that tells if the coffee machine's ready to brew.
* Raspberry Pi with camera module to extract text on coffee machine screen
* Flask app to show information


## Enable `ssh` and camera
With `Raspbian Jessie`, switch these on in `Raspberry Pi Configuration`.


## Remote `ssh` into pi

### Get pi's address in pi
```sh
hostname -I
```

### Get pi's address in remote
```sh
ifconfig | grep 'inet'
nmap -sn 192.168.2.0/24
```

### `ssh` into pi
```sh
ssh pi@192.168.2.70
```


## Setup `python`
### Some dependencies
```sh
# optional
sudo apt-get install -y unzip wget
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk2.0-dev
sudo apt-get install libatlas-base-dev gfortran # optimization of cv operations
```

```sh
# must have
sudo apt-get install python-dev python-setuptools
sudo apt-get install tesseract-ocr
```

### virtualenv
```sh
sudo pip install virtualenv
source venv/bin/activate
pip install -r req.txt
```

### Open CV (Optional)
```sh
cd ~/Libraries
git clone https://github.com/opencv/opencv_contrib.git
wget https://github.com/Itseez/opencv/archive/master.zip
unzip master.zip
rm master.zip
cd opencv-master
mkdir release
cd release
cmake -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D INSTALL_PYTHON_EXAMPLES=ON \
  -D BUILD_EXAMPLES=ON \
  -D OPENCV_EXTRA_MODULES_PATH=~/Libraries/opencv_contrib/modules ..
make -j4
sudo make install
sudo ldconfig
```

## Run
```sh
python cam.py
sudo python app.py
```
