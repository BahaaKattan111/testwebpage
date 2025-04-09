import os
from cryptography.fernet import Fernet
key = os.environ.get('MAIN_KEY')

encrypt = Fernet(key.encode('utf-8'))

with open('app.py.enc', 'rb') as file:
    file = file.read()
    decrypted_file = encrypt.decrypt(file)
    exec(decrypted_file)
