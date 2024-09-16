import streamlit as st
def render_sidebar():
    st.sidebar.title("Navigation")
    tab = st.sidebar.selectbox("Menu Campaign", ["Campaigns", "Activities", "UTM", "Vouchers", "Reports"],key='tabmain')
    
    if tab == "Campaigns":
        st.session_state['main_page'] = 'Campaigns'
    elif tab == "Activities":
        st.session_state['main_page'] = 'Activities'
    elif tab == "UTM":
        st.session_state['main_page'] = 'UTM'
    elif tab == "Vouchers":
        st.session_state['main_page'] = 'Vouchers'
    elif tab == "Reports":
        st.session_state['main_page'] = 'Reports'