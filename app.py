import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'ACcce021c33936e42582e63487099907e0'
    TWILIO_SYNC_SERVICE_SID = 'IS64cc70306026c91a6526c802e73c06bb'
    TWILIO_API_KEY = 'SKefd56806652248c2341610974f2a4f6d'
    TWILIO_API_SECRET = 'qTqQXPTrRnZ4Rx17aVrjsLmxnENIHLjv'

    username = request.args.get('username', fake.user_name())

    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad = request.form['text']
    with open('workfile.txt', 'w') as f:
        f.write(text_from_notepad)

    path_to_store_txt = "workfile.txt"

    return send_file(path_to_store_txt, as_attachment=True)

if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
