import RPi.GPIO as GPIO
import busio
import time
from adafruit_htu21d import HTU21D

sda = 2  # GPIO핀 번호
scl = 3  # GPIO핀 번호
i2c = busio.I2C(scl, sda)
sensor = HTU21D(i2c)  # HTU21D 장치를 제어하는 객체 리턴


# 온도 정보 전달용
def getTemperature():
    temperature = int(sensor.temperature)  # HTU21D 장치로부터 온도 값 읽기
    return temperature


# 습도 정보 전달용
def getHumidity():
    humidity = int(sensor.relative_humidity)  # HTU21D 장치로부터 습도 값 읽기
    return humidity



# 별도 작동용 => controller로 연결하지 않고 다수의 라즈베리파이를 사용할때

def onConnect(client, userdata, flag, rc):
    print("Connect with result code:" + str(rc))
    client.subscribe("command", qos=0)    # command라는 토픽 데이터 수신 요청
    pass



def onMessage(client, userdata, msg):
    command = str(msg.payload.decode("utf-8"))
    if command == 'temperature':
        print("온도 정보 전달 완료")
        print( getTemperature())
        client.publish(
            "temperature", getTemperature(), qos=0)
    elif command == 'humidity':
        print("습도 정보 전달 완료")
        print( getHumidity())
        client.publish("humidity", getHumidity(), qos=0)
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





