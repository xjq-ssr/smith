# -*- coding: UTF-8 -*-
#import MySQLdb
import sys
import os
from flask import Flask
from flask import render_template, redirect


app = Flask(__name__)

@app.route('/')
def onepage():
    result = os.popen('/usr/bin/python3 /home/centos/smith/geteip.py').readlines()
    ip = result[0]
    return render_template('main.html', ip=ip)

@app.route('/reset')
def reset():
    ip = os.popen('/usr/bin/python3 /home/centos/smith/changeip.py').readlines()
    return ip

@app.route('/resetip')
def resetip():
    ip = os.popen('/usr/bin/python3 /home/centos/smith/changeip.py').readlines()
    return redirect('http://' + str(ip[0]))

@app.route('/reset1')
def reset1():
    return '192.168.0.1'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
