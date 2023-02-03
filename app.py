import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import pandas as pd
from PIL import Image
import base64
from st_aggrid import AgGrid

st.set_page_config(
    page_title = 'Directorio de Convenios',
    page_icon = 'random',
    layout = 'wide'
)

@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("images/background5.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("data:image/png;base64,{img}");
background-size: cover;    
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stForm"] {{
background: rgba(218,223,225,1);
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# --- USER AUTHENTICATION ---
names = ["Anibal Angulo", "Gerardo Barajas", "Jorge Oviedo", "admin"]
usernames = ["fractalangulo", 'fractalbarajas', 'fractaloviedo', "admin"]

file_path = Path(__file__).parent / 'hashed_pw.pkl'
with file_path.open('rb') as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "modelopredictivo2", "abcdef", cookie_expiry_days=0)

# Cargar banner

a1, a2, a3 = st.columns((2.5, 8, 1))
a2.image(Image.open('images/logo.png'), width=800)
name, auhentication_status, username = authenticator.login("Login", "main")

if auhentication_status == False:
    st.error('Username or password is incorrect')

if auhentication_status == None:
    st.warning('Poner "admin" como username y "password" como password.')

if auhentication_status:
    
    a1, a2, a3 = st.columns((2.5, 8, 1))
    st.header('Directorio de convenios')
    st.subheader('Última actualización: 02/02/2023')

    # Cargar datos
    df = pd.read_csv('Directorio_Yepez2.csv', encoding='windows-1252')
    AgGrid(df)

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        label="Descargar",
        data=csv,
        file_name='Convenios_2022.csv',
        mime='text/csv',
    )