import RPi.GPIO as GPIO
import pychromecast
import time
import sys


GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)
flag = True
mc = ''


def stopCallBack(channel):
    global mc
    mc.stop()
    mc.play_media('./static/great.mp3', 'audio/mp3')
    time.sleep(30)
    global flag
    flag = False


GPIO.add_event_detect(12, GPIO.FALLING, callback=stopCallBack, bouncetime=300)


def main():
    ccast = pychromecast.get_chromecasts()
    cast = ccast[0]
    cast.wait()
    global mc
    mc = cast.media_controller
    f = open('MusicPath.txt', 'r')
    mp = f.readline()
    f.close()
    mc.play_media(mp, 'audio/mp3')
    global flag
    while flag:
        time.sleep(1)
    GPIO.cleanup()
    return 0


if __name__ == '__main__':
    sys.exit(main())
