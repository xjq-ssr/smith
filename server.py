# -*- coding: UTF-8 -*-
#import MySQLdb
import sys
import os
from flask import Flask


app = Flask(__name__)

@app.route('/')
def onepage():
    result = os.popen('/usr/bin/python3 /home/centos/smith/geteip.py').readlines()
    ip = result[0]
    return ip

@app.route('/reset')
def reset():
    result = str(os.popen('/usr/bin/python3 /home/centos/smith/main.py').readlines())
    result = '<br>'.join(r)
    return result

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
