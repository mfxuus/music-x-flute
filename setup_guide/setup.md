# Setup guide
Run those scripts on rpi4.  
````bash
sudo apt update -y
sudo apt install git -y
sudo apt-get install python3-venv -y
sudo apt-get install libatlas-base-dev -y
sudo apt-get install rpi.gpio
````

## enable I2C
````bash
sudo raspi-config
````
- "3 Interface Options"
- "I5 I2C"
- Enable? "Yes"

````bash
git clone https://github.com/mfxuus/music-x-flute.git
cd music-x-flute
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt

cd ~/music-x-flute/UI/server
sudo nano .env

mkdir ~/logs
````

## BT
````bash
bluetoothctl
power on
agent on
scan on
````
Find mac address of the BT device, and then
````bash
scan off
````

For B,  
````bash
pair 00:14:03:05:1A:20
````
For A,  
````bash
pair 00:14:03:05:18:91
````
PIN = 1234  
````bash
paired-devices
quit
````

## Running some scripts
For A,  
````bash
sudo rfcomm release all
sudo rfcomm bind 0 00:14:03:05:18:91
````

For B,  
````bash
sudo rfcomm release all
sudo rfcomm bind 0 00:14:03:05:1A:20
````

Then,  
````bash
cd ~/music-x-flute
source ./env/bin/activate
cd ~/music-x-flute/UI/server
nano .env
````
In `.env`, write the following, but fill in the IP of rpi4: 
````
WEBSOCKET_IP = '192.168.??.??'
PORT = 8765
ENV_NAME = 'PI4'
LOG_DIR = '/home/pi/logs'
````

````bash
python run_server.py
````

## Dan's problem
I cannot `import RPi` within the venv. My solution is to install pip and all dependencies outside the venv.  
````bash
cd ~
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
cd ~/music-x-flute
python -m pip install -r requirements.txt
# Now, plug in PCA9685
python ~/music-x-flute/UI/server/run_server.py
````

## flute to head
````bash
cd ~/music-x-flute
source ./env/bin/activate
python flute_to_head.py
````

## React UI
Now, leave rpi4, and go to the laptop where the frontend will be.  

````bash
cd ~/music-x-flute/UI/flute-app
nano .env.development.local
````
In `.env.development.local`, write the below, but fill in the IP addr of rpi4:  
````
REACT_APP_WEBSOCKET_SERVER=ws://192.168.??.??:8765
````

## PCA9685 pins
然后就是pin序号，不是默认位置的也要标注一下：  
https://github.com/mfxuus/music-x-flute/blob/master/controller.py#L26-L32
