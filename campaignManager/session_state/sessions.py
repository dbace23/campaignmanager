import streamlit as st
def initialize_session_state():
    
    if 'activity_groupings' not in st.session_state:
        st.session_state['activity_groupings'] = []
    if 'activity_grouping_budgets' not in st.session_state:
        st.session_state['activity_grouping_budgets'] = []
    if 'goals' not in st.session_state:
        st.session_state['goals'] = []
    if 'goal_values' not in st.session_state:
        st.session_state['goal_values'] = []
    if 'goal_options' not in st.session_state:
        st.session_state['goal_options'] = []
    if 'utm_data' not in st.session_state:
        st.session_state['utm_data'] = []
    if 'voucher_data' not in st.session_state:
        st.session_state['voucher_data'] = []
    if 'kv_data' not in st.session_state:
        st.session_state['kv_data']= []

    # Initialize session state in activities
    if 'empty_state_voucher' not in st.session_state:
        st.session_state['empty_state_voucher'] = True
    if 'empty_state_kv' not in st.session_state:
        st.session_state['empty_state_kv'] = True
    if 'main_page' not in st.session_state:
        st.session_state['main_page'] ='Campaigns'
    if 'edit_mode' not in st.session_state:
        st.session_state['edit_mode'] = False
    if 'activities_mode' not in st.session_state:
        st.session_state['activities_mode'] = False
    if 'selected_campaign' not in st.session_state:
        st.session_state['selected_campaign'] = None

