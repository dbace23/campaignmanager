import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import re

from campaign import *
 

# from google.cloud import bigquery
 
# projectId = "574810859830"
# client = bigquery.Client(project=projectId)

# Page configuration
st.set_page_config(
    page_title='AstroUTM',
    page_icon=':speech_balloon:',
    layout='wide',
    initial_sidebar_state="collapsed"
)

# Initialize dictionary for user data
d = {
    "usersId": [],
    "names": [],
    "usernames": [],
    "hashed_passwords": [],
    "divisi": [],
    "access": []
}

# global library here
#@st.cache_data(show_spinner=False)
def load_auth():
    # useraccess
    users_id = pd.read_csv('login.csv')
    users_id = users_id.drop_duplicates(subset=['id'])
    usernames = users_id['email'].values.tolist()
    passwords = users_id['password'].astype(str).values.tolist()
    hashed_passwords = stauth.Hasher(passwords).generate()
    names = users_id['name'].values.tolist()
    return usernames, hashed_passwords, names, users_id

# Function to clear the cache
def clear_cache():
    load_auth.clear()

# Load authentication data
d["usernames"], d["hashed_passwords"], d["names"], d["usersId"] = load_auth()
 
# Set up authenticator
credentials = {
    "usernames": {
        username: {"name": name, "password": hashed_password}
        for username, name, hashed_password in zip(d["usernames"], d["names"], d["hashed_passwords"])
    }
}
authenticator = stauth.Authenticate(
    credentials,
    'astromarketing',
    "astro_keys21",
    cookie_expiry_days=360
)
# Authentication
name, authentication_status, username = authenticator.login('main')

if authentication_status:
    user_data = d["usersId"][d["usersId"]['email'] == username]
    user_id = user_data['id'].values[0]
    name = user_data['name'].values[0]
    division = user_data['divisi'].values[0]
    activity = user_data['activity'].astype(str).item()
    create = user_data['create'].astype(str).item()
    approving = user_data['approval'].astype(str).item()
    
    with st.sidebar:
        authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{name}*')
   
    approving=str(approving)
    main_page(user_id, name, division, activity, create, approving)
        
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
