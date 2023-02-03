import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Anibal Angulo", "Gerardo Barajas", "Jorge Oviedo", "admin"]
usernames = ["fractalangulo", 'fractalbarajas', 'fractaloviedo', "admin"]
passwords = ['a01654684', 'a01654685', 'a01702048', 'password']

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / 'hashed_pw.pkl'
with file_path.open('wb') as file:
    pickle.dump(hashed_passwords, file)