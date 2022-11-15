# 호출어를 말한 이후에만 작동하도록

# 예를들어, 자비스! 불꺼줘! 라고 말할때, '자비스'를 앞에 붙이지 않으면 제대로 작동하지 않도록

import speech_recognition as sr
import os
import datetime
import threading

cmd_mode = False


# word가 list에 포함되어 있는지 확인
def check_item(my_list, word):
    result = False
    for token in my_list:
        if word in token:  # word가 token에 포함되어있다면
            result = True
    return result


def handle_message(msg):
    my_list = list(msg.split())
    global cmd_mode
    print(my_list, cmd_mode)
    if cmd_mode:  # 현재 입력된 명령이 cmd명령인지 아닌지 확인
        if check_item(my_list, "안녕"):
            now = datetime.datetime.now()
            say_message("지금은 %d시 %d분입니다." % (now.hour, now.minute))
    else:
        if check_item(my_list, "hello"):  # 요청어
            cmd_mode = True
            print("[[Set the command mode as True]]")  # 커멘드 모드 활성화
            # 커멘드 모드 활성화, 10초안에 명령을 내려야함 => 아니면 초기화
            start_time = threading.Timer(10, reset_mode)  # 10초후 reset
            start_time.start()


def reset_mode():
    global cmd_mode
    cmd_mode = False
    print("[[ REset the command mode as False]]")


def say_message(msg):
    print(msg)
    os.system(msg)


while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("say something!")
        audio = r.listen(source)

    try:
        msg = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said : " + msg)
        handle_message(msg)  # 사용자의 음성을 handle_message로 보냄
    except sr.UnknownValueError:
        print("오류 발생")
    except sr.RequestError as e:
        print("d오류 발생")
