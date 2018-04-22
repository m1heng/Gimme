import serial
import time


ser = serial.Serial('/dev/tty.usbmodem1411', 9600)

while True:
	ser.write(0)
	time.sleep(5)
