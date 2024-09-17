import streamlit as st
from datetime import date, timedelta, datetime
from campaignManager.utils.utils import *
from campaignManager.query.query import *

def activity_table(user_id,name,division,activity,create,approving,activitiesdf,campaigns):
    st.title("Activities Manager")
     
    campaigns=campaigns[(campaigns['approval'] == True) & (campaigns['end_date'] > pd.Timestamp(date.today()))]    #cara load campaigns with this condition
 
    act_group=activitiesdf['activity_grouping'].unique()

    campaigns['campaign_id_name'] = campaigns['campaign_id'] + "_" + campaigns['campaign_name']
    campaign_names = campaigns['campaign_id_name'].unique()

    
    if len(campaign_names)==0: #check if there's approved items
        st.write("No campaigns available.")
        apc=False
    else:
        apc=True
        selected_campaign = st.selectbox('Filter by Campaign', ['All'] + list(campaign_names))
        actcols=st.columns([1,1,1])
        with actcols[0]:activity_status=st.selectbox('activity status',('all','pending approving','rejected','ongoing','ended'))
        with actcols[1]:activity_grouping=st.selectbox('activity grouping',(['All']+list(act_group)))
        with actcols[2]:activity_creator=st.selectbox('actvity creator',['All']+list(activitiesdf['created_by_username'].unique()))

        if selected_campaign!='All':filtered_act=activitiesdf[activitiesdf['campaign_id']==selected_campaign.split("_")[0]]
        else:filtered_act=activitiesdf

        if activity_status=='All':filtered_act=filtered_act
        elif activity_status=='pending approving':filtered_act=filtered_act[filtered_act['approval']==None]
        elif activity_status=='rejected':filtered_act=filtered_act[filtered_act['approval']==False]
        elif activity_status=='ongoing':filtered_act=filtered_act[(filtered_act['approval']==True) & (filtered_act['end_date'] <= pd.Timestamp(date.today()))]
        elif activity_status=='ended':filtered_act=filtered_act[(filtered_act['approval']==True) & (filtered_act['end_date'] >= pd.Timestamp(date.today()))]
        
        if activity_creator!='All':filtered_act=filtered_act[filtered_act['created_by']=='activity_creator']
        else:filtered_act=filtered_act
        
#################aproval
        approvalbutton=False
        if  ',' in approving:
            approving=str(approving)  
            approving_list = list(map(int, str(approving).split(',')))
            jmlhapproval = len(filtered_act[
                                                    (filtered_act['created_by_userid'].isin(approving_list)) &  # First condition: user ID in approving_list
                                                    (filtered_act['approval'] != True)  # Second condition: approval is not True
                                                ])
            
            if jmlhapproval>0:
                approvalbutton=st.toggle(f'{jmlhapproval} campaigns pending your approval')
                if approvalbutton:
                    filtered_act = filtered_act[filtered_act['created_by_userid'].isin(approving_list)]

        # Pagination
        if approving:page_size=5
        else:page_size = 10
        total_items = len(filtered_act)
        total_pages = (total_items // page_size)  
        
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = 1

        def change_page(page):
            st.session_state['current_page'] = page    
        
        current_page = st.session_state['current_page']
        start_idx = (current_page - 1) * page_size
        end_idx = start_idx + page_size
        filtered_act = filtered_act.iloc[start_idx:end_idx]
 
        activity_event = st.dataframe(filtered_act[['activity_id','activity_grouping','activity_name','activity_details','start_date','end_date','approval']],hide_index=True,on_select="rerun",selection_mode="multi-row")
        
        if total_pages>1:
            col1, col2, col3 = st.columns(3)
            with col1:
                if current_page!=1:
                    if st.button('Previous'):
                        if current_page > 1:
                            change_page(current_page - 1)
                            st.rerun()
            with col2:
                st.write(f"Page {current_page} of {total_pages}")
            with col3:
                if current_page!=total_pages:
                    if st.button('Next'):
                            if current_page < total_pages:
                                change_page(current_page + 1)
                                st.rerun()
 

        try:
            act=activity_event['selection']['rows'] 
            selected_activity_id=filtered_act.iloc[act]['activity_id'].item()
            if approvalbutton:
                notesdariapproval=st.text_input('Notes(optional)')
                acol=st.columns([1,1,5])
                with acol[0]:
                    if st.button('approve'):
                        approval=True
                        update_activity_button_p(selected_activity_id,notesdariapproval,approval,user_id,name)
                        st.rerun()

                with acol[1]:
                    if st.button('reject'):
                        approval=False
                        update_activity_button_p(selected_activity_id,notesdariapproval,approval,user_id,name)
                        st.rerun()
        except Exception as e:pass
        return approvalbutton,apc
