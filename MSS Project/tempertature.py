import RPi.GPIO as GPIO
import busio
from adafruit_htu21d import HTU21D

sda = 2  # GPIO핀 번호
scl = 3  # GPIO핀 번호
i2c = busio.I2C(scl, sda)
sensor = HTU21D(i2c)  # HTU21D 장치를 제어하는 객체 리턴


# 온습도 정보 전달용
def getTemperatureAndHumidity():
    temperature = int(sensor.temperature)  # HTU21D 장치로부터 온도 값 읽기
    humidity = float(sensor.relative_humidity)  # HTU21D 장치로부터 습도 값 읽기
    return temperature  # 우선 온도 정보만
# , humidity  # 온습도 정보 리턴
