import pandas as pd
import streamlit as st
import random
import string




def format_rupiah(value):
    return "Rp {:,.0f}".format(value)

def generate_random_alphanumeric(length=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def clear_goals():
    st.session_state['goals'] = []
    st.session_state['goal_values'] = []
    st.session_state['goal_options'] = []

def clear_budgets():
    st.session_state['activity_groupings'] = []
    st.session_state['activity_grouping_budgets'] = []

def load_data_approved_campaigns():
    try:
        campaignsdf = pd.read_csv('campaigns.csv')
        campaignsdf['start_date'] = pd.to_datetime(campaignsdf['start_date'])
        campaignsdf['end_date'] = pd.to_datetime(campaignsdf['end_date'])
        campaignsdf['campaign_total_budget']= campaignsdf['campaign_total_budget'].astype(int)
        
    except FileNotFoundError:
        st.error('hubungi halim')
    return campaignsdf