# https://forums.raspberrypi.com/viewtopic.php?t=214373
# sudo rfcomm bind 0 00:14:03:05:08:7F
sudo rfcomm release all
sudo rfcomm bind 0 00:14:03:05:08:7F
# https://forums.raspberrypi.com/viewtopic.php?p=919463#p919463

import socket
hostMACAddress = 'DC:A6:32:73:0F:D7'
# hostMACAddress = '00:14:03:05:08:7F'
port = 3
size = 1024
s = socket.socket(
    socket.AF_BLUETOOTH,
    socket.SOCK_STREAM,
    socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress, port))
s.listen(1)


def new_client(client):
    while 1:
        data = client.recv(size)
        if data:
            n = data.decode("utf-8")
            print(n)
            client.send(data)


client, address = s.accept()
new_client(client)







import socket
server_address = "DC:A6:32:73:0F:D7"
server_address = "00:14:03:05:08:7F"
server_port = 3
c = socket.socket(
    socket.AF_BLUETOOTH,
    socket.SOCK_STREAM,
    socket.BTPROTO_RFCOMM)
c.connect((server_address, server_port))
c.send(b"desserts")
print(c.recv(1024).decode())





import serial
btSerial = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=0.5)


btSerial.write(b"Hi")

while True:
    data = btSerial.readline()
    if data:
        print(data)
