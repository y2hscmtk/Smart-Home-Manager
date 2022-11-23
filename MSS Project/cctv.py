# publisher/subscriber
import time
import paho.mqtt.client as mqtt
import mycamera  # 카메라 사진 보내기

flag = False


def on_connect(client, userdata, flag, rc):
    client.subscribe("command", qos=0)


def on_message(client, userdata, msg):
    global flag
    command = msg.payload.decode("utf-8")
    if command == "cctvOn":
        print("cctv On")
        flag = True
    elif command == "cctvOff":
        print("cctv Off")
        flag = False


if __name__ == '__main__':
    broker_ip = "localhost"  # 현재 이 컴퓨터를 브로커로 설정
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_ip, 1883)
    client.loop_start()
    while True:
        if flag:
            imageFileName = mycamera.takePicture()  # 카메라 사진 촬영
            print(imageFileName)
            client.publish("mjpeg", imageFileName, qos=0)
        time.sleep(0.5)
    client.loop_end()
    client.disconnect()
