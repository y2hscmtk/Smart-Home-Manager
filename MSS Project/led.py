import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 6  # 핀 번호 GPIO6 의미, 빵판하단 16번 홀

GPIO.setup(led, GPIO.OUT)  # GPIO 6번 핀을 출력 선으로 지정.


# led 작동용
def ledOnOff(onOff):
    global led
    GPIO.output(led, onOff)
