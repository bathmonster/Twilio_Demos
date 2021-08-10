from flask import Flask
from flask import json
from flask import request


app = Flask(__name__)

@app.route('/')
def api_root():
   return 'Welcome'

@app.route('/twilio' , methods=['POST'])
def api_twilio_message():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        return json.dumps(request.json)

if __name__ == '__main__':
    app.run(debug=True)