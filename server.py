# -*- coding: UTF-8 -*-
#import MySQLdb
import sys
import os
from flask import Flask
from flask import 
from flask import render_template


app = Flask(__name__)

@app.route('/')
def onepage():
    result = os.popen('/usr/bin/python3 /home/centos/smith/geteip.py').readlines()
    ip = result[0]
    return render_template('button.html', ip=ip)

@app.route('/reset')
def reset():
    ip = os.popen('/usr/bin/python3 /home/centos/smith/changeip.py').readlines()
    return ip

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
