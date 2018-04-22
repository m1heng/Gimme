import serial
import time


ser = serial.Serial('/dev/tty.usbmodem1411', 9600)

while True:
	ser.write('2'.encode())
	some  =  ser.read(size = 10)
	print(some)
	time.sleep(1)
