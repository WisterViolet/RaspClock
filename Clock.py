import sys
import datetime as dt
import Twipost
import subprocess
import time
import RPi.GPIO as GPIO

AlarmTime = dt.time(0, 00)
MusicPath = ''
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)


def setAlarm():
    with open('AlarmTime.txt', 'r') as f:
        tInfo = f.readline().split(':')
        global AlarmTime
        AlarmTime = dt.time(int(tInfo[0]),
                            int(tInfo[1]))
    print(AlarmTime)


def stepTime(step, num):
    t = []
    for i in range(num):
        t.append(dt.timedelta(minutes=step*(i+1)))
    return t


def clocking():
    setAlarm()
    flag = True
    cnt = 0
    bflag = True
    # button chack
    TweetTime = stepTime(1, 10)
    print(TweetTime)
    while(True):
        if GPIO.input(11) == GPIO.LOW:
            bfag = True
        else:
            bflag = False
        cnt += 1
        if cnt == 3000:
            setAlarm()
            cnt = 0
        now = dt.datetime.now()
        if now.minute == AlarmTime.minute and bflag:
            if flag:
                flag = False
                if(now.hour == AlarmTime.hour):
                    print('A')
                    proc = subprocess.Popen(['python3','Ringing.py'], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                    Twipost.Twi_aupos("Asa!")
        else:
            if flag and bflag:
                for t in TweetTime:
                    bTime = now-t
                    if ((bTime.hour == AlarmTime.hour) and
                       (bTime.minute == AlarmTime.minute)):
                        flag = False
                        print('B')
                        Twipost.Twi_aupos('{}minutes late'.format(int(t.seconds/60)))
            else:
                flag = True
                for t in TweetTime:
                    bTime = now-t
                    bTime = now-t
                    if ((bTime.hour == AlarmTime.hour) and
                       (bTime.minute == AlarmTime.minute)):
                        flag = False
        time.sleep(0.2)


if __name__ == '__main__':
    clocking()
