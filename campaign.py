import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime
import random
import string

from campaignManager.session_state.sessions import *
from campaignManager.campaign.campaign_main_page import *
from campaignManager.campaign.campaign_items import *
from campaignManager.activities.activity_main_page import *
from campaignManager.activities.activity_items import *
from campaignManager.utm.new_utm import *
from campaignManager.query.query import *

def main_page(user_id,name,division,activity,create,approving):
 
    # Initialize session state
    initialize_session_state()
 
    if st.session_state['main_page'] == 'Create New Campaign':
        campaign_item(user_id,name,division)
    
    if st.session_state['main_page'] == 'Create New Activity':
         campaigns,approvedbudget,approvedgoals=load_data_approved_activities()
         activityitem(user_id,name,division,campaigns,approvedbudget,approvedgoals)

    if st.session_state['main_page'] == 'Create New UTM':
        activitiesdf,error = load_data_activities()
        new_utm(activitiesdf,user_id,name)
    
    else:
        words_create = ['Create New Campaign', 'Create New Activity']
        if all(word not in st.session_state['main_page'] for word in words_create):
            tab = st.sidebar.selectbox("Menu Campaign", st.session_state['dynamic_menu'])
            st.session_state['main_page']=tab
         
            
            if tab == "Campaigns" or st.session_state['main_page'] == 'Campaigns':
                #load library
                campaignsdf,error = load_data_campaigns()
                if error=="200": 
                    appovalbutton = campaign_table(user_id,name,division,activity,create,approving,campaignsdf)

                    if 'campaigns' in str(create) and not appovalbutton:
                        if st.button('Create New Campaign'):
                            st.session_state['main_page'] = 'Create New Campaign'
                            st.rerun()
                else:
                    st.error(error)
            
            elif tab == "Activities" or st.session_state['main_page'] == 'Activities':
                campaigns,approvedbudget,approvedgoals=load_data_approved_activities()
                activitiesdf,error = load_data_activities()
                if error=="200": 
                    appovalbutton,apc =activity_table(user_id,name,division,activity,create,approving,activitiesdf,campaigns)
                    if apc:
                      if 'activities' in str(create) and not appovalbutton:
                          if st.button('Create New Activity'):
                              st.session_state['main_page'] = 'Create New Activity'
                              st.rerun()
                else:
                    st.error(error)
            
            elif tab == "UTM" or st.session_state['main_page'] == 'UTM':
                utmdf=load_utm()

                st.subheader('UTM')
                if st.button('➕ utm'):
                    st.session_state['main_page'] = 'Create New UTM'
                    st.rerun()
          
