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
    app.run(host='0.0.0.0', port=80)
