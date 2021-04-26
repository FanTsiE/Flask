import serial
from time import sleep

baudrate = 9600
ser1= serial.Serial("COM1", baudrate,write_timeout=1)
msg=["024F4E0D03","02 4F 46 0D 03", "0255313233340D03", "02 49 37 35 0D 03", "02 55 53 0D 03", "02 49 53 0D 03"]


# send data to COM2
for i in range(6):
    ser1.write(bytes.fromhex(msg[i]))


# read data COM2 sends back
while True:
    msg_back = ser1.readline()
    if len(msg_back) >= 1:
        print(msg_back)
