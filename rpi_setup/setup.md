sudo apt update -y
sudo apt install git -y
sudo apt-get install python3-venv -y
sudo apt-get install libatlas-base-dev -y

<!-- enable I2C -->
sudo raspi-config
<!-- "3 Interface Options" -->
<!-- "I5 I2C" -->
<!-- Enable? "Yes" -->

git clone https://github.com/mfxuus/music-x-flute.git
cd music-x-flute
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt

cd ~/music-x-flute/UI/server
sudo nano .env


mkdir ~/logs



# BT
bluetoothctl
power on
agent on
scan on
<!-- Find mac address of the BT device, then scan off -->
scan off

# B
pair 00:14:03:05:1A:20
# A
pair 00:14:03:05:18:91
paired-devices
quit



<!-- Running some scripts -->
# A
sudo rfcomm release all
sudo rfcomm bind 0 00:14:03:05:18:91


# B
sudo rfcomm release all
sudo rfcomm bind 0 00:14:03:05:1A:20

cd ~/music-x-flute
source ./env/bin/activate
cd ~/music-x-flute/UI/server
# sudo nano .env
python run_server.py


cd ~/music-x-flute
source ./env/bin/activate
python flute_to_head.py