import sys
import io
import time
import paho.mqtt.client as mqtt
# from adafruit_htu21d import HTU21D
# import RPi.GPIO as GPIO
import temperature
import led
import guestCheck

###
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
        return render_template('12-3image.html')

app.run(host='0.0.0.0', port=8080)


###


# AI Speaker에서 mqtt로 보낸 command에 맞춰 명령을 처리하는 중앙 장치


# mqtt 사용용
def onConnect(client, userdata, flag, rc):
    print("Connect with result code:" + str(rc))
    client.subscribe("command", qos=0)    # command라는 토픽 데이터 수신 요청
    pass


def onMessage(client, userdata, msg):
    command = str(msg.payload.decode("utf-8"))
    # if (command == 'start'):
    #     isStarted = True
    if command == 'temperature':
        print("온도 정보 전달 완료")
        print(temperature.getTemperatureAndHumidity())
        client.publish(
            "temperature", temperature.getTemperatureAndHumidity(), qos=0)
    elif (command == 'ledOn'):
        led.ledOnOff(True)      # LED ON
    elif (command == 'ledOff'):
        led.ledOnOff(False)   # LED OFF
    pass


broker_address = "localhost"

client = mqtt.Client()
client.on_connect = onConnect
client.on_message = onMessage

client.connect(broker_address, 1883)
client.loop_start()

while (True):
    distance = guestCheck.measureDistance()
    if distance < 50:  # 물체가 일정거리 이상 가까워질경우 => 손님방문
        print("손님 방문")
        client.publish("guest", distance, qos=0)
        time.sleep(10)  # 손님 방문사실을 알린 이후, 중복 메세지를 보내지 않도록 하기 위함

    # 손님 방문 확인 시스템

client.disconnect()
