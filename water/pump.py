import RPi.GPIO as GPIO

PIN = 2

class Pump():
    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.OUT)
        GPIO.output(PIN, GPIO.HIGH)
        self.current = GPIO.HIGH
        
    def flow(self):
        if self.current == GPIO.LOW:
            return
       
        GPIO.output(PIN, GPIO.LOW)
        self.current = GPIO.LOW

    def stop(self):
        if self.current == GPIO.HIGH:
            return
        
        GPIO.output(PIN, GPIO.HIGH)
        self.current = GPIO.HIGH
       
    def shutdown(self):
        GPIO.cleanup()