import RPi.GPIO as GPIO

RELAY_PINS = {"pumpe": 17, "uv": 27, "salz": 22}


class RelayControl:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        for pin in RELAY_PINS.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def set_relay(self, name, state):
        pin = RELAY_PINS.get(name)
        if pin is not None:
            GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()
