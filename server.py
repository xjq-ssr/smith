# -*- coding: UTF-8 -*-
#import MySQLdb
import sys
import os
from flask import Flask


app = Flask(__name__)

@app.route('/')
def onepage():
    result = os.popen('/usr/bin/python3 /home/centos/smith/geteip.py').readlines()
    return result

@app.route('/reset')
def reset():
    result = os.popen('/usr/bin/python3 /home/centos/smith/main.py').readlines()
    return result

if __name__ == '__main__':
    app.debug = True
    app.jinjia_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=80)
