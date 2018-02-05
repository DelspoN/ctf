# uncompyle6 version 2.12.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: back.py
# Compiled at: 2017-10-05 17:09:10
import sys
import os
import time
from flask import Flask
from flask import request
from flask import abort
import hashlib

def check_creds(user, pincode):
    if len(pincode) <= 8 and pincode.isdigit():
        val = '{}:{}'.format(user, pincode)
        key = hashlib.sha256(val).hexdigest()
        if key == '34c05015de48ef10309963543b4a347b5d3d20bbe2ed462cf226b1cc8fff222e':
            return 'Congr4ts, you found the b@ckd00r. The fl4g is simply : {}:{}'.format(user, pincode)
    return abort(404)


app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>HOME</h1>'


@app.route('/backdoor')
def backdoor():
    user = request.args.get('user')
    pincode = request.args.get('pincode')
    return check_creds(user, pincode)


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=3333)