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


# 별도 작동용 => controller로 연결하지 않고 다수의 라즈베리파이를 사용할때

def onConnect(client, userdata, flag, rc):
    print("Connect with result code:" + str(rc))
    client.subscribe("command", qos=0)    # command라는 토픽 데이터 수신 요청
    pass


def onMessage(client, userdata, msg):
    command = str(msg.payload.decode("utf-8"))
    if (command == 'ledOn'):
        ledOnOff(True)      # LED ON
    elif (command == 'ledOff'):
        ledOnOff(False)   # LED OFF
    pass


# import 되지않고, 별도의 라즈베리파이에서 작동하는 상황을 가정
if __name__ == '__main__':
    import paho.mqtt.client as mqtt
    # mqtt 사용용

    broker_address = "localhost"

    client = mqtt.Client()
    client.on_connect = onConnect
    client.on_message = onMessage

    client.connect(broker_address, 1883)
    client.loop_start()

    while (True):
        time.sleep(0.1)  # 프로그램 종료 방지용

