# -*-coding:utf-8-*-
import os
import datetime as dt
import time
import bottle
import Twipost

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')


@bottle.route('/menu', method='GET')
def menuGet():
    time_IsSet = False
    if bottle.request.query:
        time_IsSet = True
        AlarmTime = dt.time(int(bottle.request.query['Hour']),
                            int(bottle.request.query['Minute']))
        with open('AlarmTime.txt', 'w') as f:
            f.write(f'{AlarmTime.hour}:{AlarmTime.minute}')
    return bottle.template('menu_get', time_IsSet=time_IsSet,
                           music_IsSet=False)


@bottle.route('/menu', method='POST')
def menuGetM():
    music_IsSet = False
    badfile_IsSet = False
    upload = bottle.request.files.get('upload')
    if not upload.filename.lower().endswith('.mp3'):
        badfile_IsSet = True
        return bottle.template('menu_music', badfile_IsSet=badfile_IsSet)
    SAVE_DIR = os.path.join(BASE_DIR, f'static/{upload.filename}')
    upload.save(SAVE_DIR, overwrite=True)
    with open('MusicPath.txt', 'w') as f:
        f.write(str(SAVE_DIR))
    music_IsSet = True
    return bottle.template('menu_get', music_IsSet=music_IsSet,
                           time_IsSet=False)


@bottle.route('/time')
def timeSet():
    return bottle.template('menu_time')


@bottle.route('/music')
def timeSet():
    return bottle.template('menu_music', badfile_IsSet=False)


@bottle.route('/static/css')
def getCSS():
    return bottle.static_file('style.css', root=f'{STATIC_DIR}')


@bottle.route('/static/<filename:path>')
def getPicture(filename):
    return bottle.static_file(filename, root=f'{STATIC_DIR}')


@bottle.error(404)
def notFound(error):
    return str(404)


def running():
    bottle.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    running()
