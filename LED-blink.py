#!/usr/bin/python

import socket
import time
import RPi.GPIO as GPIO

HOST = "127.0.0.1"
PORT = 30003

LED = 18 # GPiO Port
LIGHT_ON = 0.1  # Second

# Initialize GPiO port
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)


# Main loop, checks if the port is down and tries to do a new connection
def main():
   s = connect()

   while 1:
      try:
         data = s.recv(1024)
         if len(data) == 0:
            print('Lost connection, trying to reconnect')
            s.close()
            s = connect()

         blink()
         # Uncomment the line below if you like to see the raw data.
         #print data.strip()

      except socket.error:
         print('Lost connecttion, reconnecting')
         s = connect()


# Well it blinks, a short one.
def blink():
   GPIO.output(LED, GPIO.HIGH)
   time.sleep(LIGHT_ON)
   GPIO.output(LED, GPIO.LOW)


# Do a connection to a socket, if the server is down wait 10 seconds and try again.
def connect():
   while 1:
      try:
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         s.connect((HOST, PORT))
         print("Connected to dump1090 on %s:%i" % (HOST, PORT))
         return s
      except socket.error:
         print("Cant connect to dump1090 on %s:%i, trying again in 10" % (HOST, PORT))
         time.sleep(10)


# Run the code untill CRTL-C is pressed. Then resets the GPIO-pin and exits nicely.
if __name__ == '__main__':
   try:
      main()
   except KeyboardInterrupt:
      GPIO.cleanup()
      print 'Exiting!'
      exit()
