import sys
import io
import time
import paho.mqtt.client as mqtt
# from adafruit_htu21d import HTU21D
import temperature
import led

# AI Speaker에서 mqtt로 보낸 command에 맞춰 명령을 처리하는 중앙 장치

# # 초음파제어
# trig = 20  # 빵판으로는 상단19번
# echo = 16  # 빵판으로는 상단18번

# GPIO.setup(trig, GPIO.OUT)
# GPIO.setup(echo, GPIO.IN)
# GPIO.output(trig, False)


# mqtt 사용용
def onConnect(client, userdata, flag, rc):
    print("Connect with result code:" + str(rc))
    client.subscribe("command", qos=0)    # command라는 토픽 데이터 수신 요청
    pass


def onMessage(client, userdata, msg):
    global autoLight, lightOnOff
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
    elif (command == 'distance'):
        # 거리 송출에 대한 ON/OFF
        isDistance = True if isDistance == False else False
    pass


broker_address = "localhost"

client = mqtt.Client()
client.on_connect = onConnect
client.on_message = onMessage

client.connect(broker_address, 1883)
client.loop_start()

while (True):
    time.sleep(0.1)  # 프로그램 종료 방지용

    # 손님 방문 확인 시스템

    # 거리 송신에 대한 요청이 있으면
    # if (isDistance == True):
    #     client.publish("distance", str(distance), qos=0)
    #     pass

client.disconnect()
