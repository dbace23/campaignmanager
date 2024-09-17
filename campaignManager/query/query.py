import pandas as pd
import streamlit as st
from datetime import datetime,date

now=datetime.now()

#page campaign 
def load_data_campaigns():
    try:
        campaignsdf = pd.read_csv('campaigns.csv')
        campaignsdf['start_date'] = pd.to_datetime(campaignsdf['start_date'])
        campaignsdf['end_date'] = pd.to_datetime(campaignsdf['end_date'])
        campaignsdf['campaign_total_budget']= campaignsdf['campaign_total_budget'].astype(int)
        error="200"        
    except:
        campaignsdf=pd.DataFrame()
        error="query:load_data_campaigns() not working"
    return campaignsdf,error

def save_campaign(campaigndf, goals_df, activity_df):
    campaigndf.to_csv('campaigns.csv', index=False)
    goals_df.to_csv('goals.csv', index=False)

    activity_df[['report_status','reported_cost','report_leads_attachment','report_other_attachment','report_pr_attachment']]=None
    activity_df.to_csv('activity_budget.csv', index=False)

def load_all_goals(): 
    selectedgoals=pd.read_csv('goals.csv')
    return selectedgoals

def load_all_budget():
    selectedbudgetdf=pd.read_csv('activity_budget.csv')
    return selectedbudgetdf

def update_campaign_button_p(selected_campaign_id,notes,approval,user_id,name):
    campaignsdf = pd.read_csv('campaigns.csv')
  
    campaignsdf['approval']=campaignsdf['approval'].astype(bool)
    campaignsdf['approved_by_username']=campaignsdf['approved_by_username'].astype(str)
    campaignsdf['approved_at']=campaignsdf['approved_at'].astype(str)
    campaignsdf['notes']=campaignsdf['notes'].astype(str)
    
    if len(notes)>0:
        campaignsdf.loc[campaignsdf['campaign_id'] == selected_campaign_id, 'notes'] = notes
    campaignsdf.loc[campaignsdf['campaign_id'] == selected_campaign_id, 'approval'] = approval
    campaignsdf.loc[campaignsdf['campaign_id'] == selected_campaign_id, 'approved_by_userid'] = user_id
    campaignsdf.loc[campaignsdf['campaign_id'] == selected_campaign_id, 'approved_by_username'] = name
    campaignsdf.loc[campaignsdf['campaign_id'] == selected_campaign_id, 'approved_at'] = now

    campaignsdf.to_csv('campaigns.csv')

##################activity page
def load_data_approved_activities():
    campaigns = pd.read_csv('campaigns.csv')
    campaigns['end_date']=pd.to_datetime(campaigns['end_date'])
    campaigns=campaigns[(campaigns['approval'] == True) & (campaigns['end_date'] > pd.Timestamp(date.today()))] 

    budget=pd.read_csv('activity_budget.csv')
    budget=budget[budget['campaign_id'].isin(campaigns['campaign_id'])]

    goals=pd.read_csv('goals.csv')
    goals=goals[goals['campaign_id'].isin(campaigns['campaign_id'])]

    return campaigns,budget,goals 

def load_data_activities():
    try:
        activitiesdf = pd.read_csv('activity.csv')
        error="200"        
    except:
        activitiesdf =pd.DataFrame()
        error="query:load_data_activities() not working"
    return activitiesdf,error


def save_activity(activitydf,goals_df,utmdf,promodf,kvdf):
    activitydf.to_csv('activity.csv', index=False)
    goals_df.to_csv('goals.csv', index=False)
    if len(utmdf)>0:
        utmdf.to_csv('utm.csv', index=False)
    if len(promodf)>0:
        promodf.to_csv('promo.csv', index=False)
    if len(kvdf)>0:
        kvdf.to_csv('kv.csv', index=False)

def  update_activity_button_p(selected_activity_id,notes,approval,user_id,name):

    pass
    activitydf = pd.read_csv('activity.csv')
  
    activitydf['approval']=activitydf['approval'].astype(bool)
    activitydf['approved_by_username']=activitydf['approved_by_username'].astype(str)
    activitydf['approved_at']=activitydf['approved_at'].astype(str)
    activitydf['notes']=activitydf['notes'].astype(str)
    
    if len(notes)>0:
        activitydf.loc[activitydf['activity_id'] == selected_activity_id, 'notes'] = notes
    activitydf.loc[activitydf['activity_id'] == selected_activity_id, 'approval'] = approval
    activitydf.loc[activitydf['activity_id'] == selected_activity_id, 'approved_by_userid'] = user_id
    activitydf.loc[activitydf['activity_id'] == selected_activity_id, 'approved_by_username'] = name
    activitydf.loc[activitydf['activity_id'] == selected_activity_id, 'approved_at'] = now

    activitydf.to_csv('activity.csv')

#utm

def load_utm():
    utmdf=pd.read_csv('utm.csv')
    return utmdf