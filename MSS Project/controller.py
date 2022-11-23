import sys
import io
import time
import paho.mqtt.client as mqtt
# cctv 작동용
import mycamera  # 카메라 사진 보내기
import threading
import cv2

# 외부 모듈 import
import temperature
import led
import guestCheck

# 카메라 제어용
isStarted = False

# AI Speaker에서 mqtt로 보낸 command에 맞춰 명령을 처리하는 중앙 장치

# 손님 방문 사실 알림 여부를 저장
guest = True


# 손님 방문 알림에 대한 정보를 리셋
def reset_guest():
    global guest
    guest = True

# mqtt 사용용


def onConnect(client, userdata, flag, rc):
    print("Connect with result code:" + str(rc))
    client.subscribe("command", qos=0)    # command라는 토픽 데이터 수신 요청
    pass


# command에 대응
def onMessage(client, userdata, msg):
     global isStarted
    command = str(msg.payload.decode("utf-8"))

    if command == 'temperature':
        print("온도 정보 전달 완료")
        print(temperature.getTemperature())
        client.publish(
            "temperature", temperature.getTemperature(), qos=0)
    elif command == "humidity":
        print("습도 정보 전달완료")
        print(temperature.getHumidity())
        client.publish("humidity", temperature.getHumidity(), qos=0)

    elif command == 'ledOn':
        led.ledOnOff(True)      # LED ON
    elif command == 'ledOff':
        led.ledOnOff(False)   # LED OFF

    elif command == 'cctvOn':
        print("cctv start!")
        isStarted = True
    elif command == 'cctvOff':
        print(("cctv stop!"))
        isStarted = False
    pass


broker_address = "localhost"

client = mqtt.Client()
client.on_connect = onConnect
client.on_message = onMessage

client.connect(broker_address, 1883)
client.loop_start()


while True:
    # cctv 사진 송출 시스템
    if isStarted:
        imageFileName = mycamera.takePicture()  # 카메라 사진 촬영
        print(imageFileName)
        client.publish("mjpeg", imageFileName, qos=0)
    time.sleep(0.5)

    # 손님 방문 알림 시스템
    distance = guestCheck.measureDistance()
    if distance < 50:  # 물체가 일정거리 이상 가까워질경우 => 손님방문
        if guest == True:  # 손님 방문사실을 여러번 알리는것을 방지하기 위함
            print("손님 방문")
            isStarted = True # 손님 방문시 카메라 켜기
            client.publish("guest", distance, qos=0)
            guest = False  # 재알림 방지
            start_time = threading.Timer(60, reset_guest)  # 1분 후 알림정보 리>
            start_time.start()

client.disconnect()


