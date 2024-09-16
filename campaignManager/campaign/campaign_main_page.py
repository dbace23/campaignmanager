import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime

from campaignManager.utils.utils import *
from campaignManager.query.query import *


def campaign_table(user_id,name,division,activity,create,approving,campaignsdf):
    st.title("Campaign Manager")
  
    if campaignsdf.empty:
        st.write("No campaigns available.")
        selectmodecampaign = False
    else:
        #load logic for activities
        campaignsdf['Pending Activities'] = 0  # Placeholder for pending activities count
        campaignsdf['Ongoing Activities'] = 0  # Placeholder for ongoing activities count
        campaignsdf['report_status']=None

        #filter
        filcol=st.columns([1,1,1,1])
        #date filter
        with filcol[0]:
            maxval = max(campaignsdf['end_date'])
            minval =min(campaignsdf['start_date'])
            try:
                startDateCampaign, endDateCampaign = st.date_input("Start date-end date", [minval, maxval], min_value=minval, help="choose campaign date filter")
                startDateCampaign = datetime.combine(startDateCampaign, datetime.min.time())
                endDateCampaign = datetime.combine(endDateCampaign, datetime.min.time())
            except Exception as e:
                st.error(f'Choose the dates {e}')
        #created by filter
        with filcol[1]:created_filter=st.multiselect('campaign creator',campaignsdf['created_by_username'].unique(),campaignsdf['created_by_username'].unique()[0])
        #campaign_status
        with filcol[2]:campaign_status=st.selectbox('campaign status',('all','pending approving','rejected','ongoing','ended'))
        #report submitted
        with filcol[3]:report_status=st.selectbox('report status',('all','pending','submitted','verified'))
        
        #filter df
        filter_campaignsdf = campaignsdf[
            (campaignsdf['start_date'] >= startDateCampaign) &
            (campaignsdf['end_date'] <= endDateCampaign) &
            (campaignsdf['created_by_username'].isin(created_filter))
        ]
        # Apply campaign status filter
        if campaign_status == 'pending approving':
            filter_campaignsdf = filter_campaignsdf[filter_campaignsdf['approving'].isna()]
        elif campaign_status == 'rejected':
            filter_campaignsdf = filter_campaignsdf[filter_campaignsdf['approving'] == False]
        elif campaign_status == 'ongoing':
            filter_campaignsdf = filter_campaignsdf[(filter_campaignsdf['start_date'] <= pd.Timestamp(date.today())) & (filter_campaignsdf['end_date'] >= pd.Timestamp(date.today())) & (filter_campaignsdf['approving'] == True)]
        elif campaign_status == 'ended':
            filter_campaignsdf = filter_campaignsdf[(filter_campaignsdf['end_date'] < pd.Timestamp(date.today()))& (filter_campaignsdf['approving'] == True)]

        #apply report status filter
        if report_status=='pending':    
            filter_campaignsdf=filter_campaignsdf[filter_campaignsdf['report_status']=='pending']
        if report_status=='submitted':
            filter_campaignsdf=filter_campaignsdf[filter_campaignsdf['report_status']=='submitted']
        if report_status=='verified':    
            filter_campaignsdf=filter_campaignsdf[filter_campaignsdf['report_status']=='verified']

        
        if campaign_status in ('all','ongoing','ended'):
            #score card
            budget_absorption = 0  # Placeholder for ongoing activities count
            total_budget=0
            newreg=0
            newbuyer=0
            gmv=0
            if total_budget>0:
                sccol=st.columns([1,1,1,1,1])
                with sccol[0]:st.metric(label="total budget", value=format_rupiah(total_budget))
                with sccol[1]:st.metric(label="budget absorption", value=budget_absorption)
                with sccol[2]:st.metric(label="new register", value=newreg)
                with sccol[3]:st.metric(label="new buyer", value=newbuyer)
                with sccol[4]:st.metric(label="GMV", value=gmv)
        
        #approval
        approvalbutton=False
        if  ',' in approving:   
            approving=str(approving)  
            approving_list = list(map(int, str(approving).split(',')))
            jmlhapproval = len(filter_campaignsdf[
                                                    (filter_campaignsdf['created_by_userid'].isin(approving_list)) &  # First condition: user ID in approving_list
                                                    (filter_campaignsdf['approval'] != True)  # Second condition: approval is not True
                                                ])
            if jmlhapproval>0:
                approvalbutton=st.toggle(f'{jmlhapproval} campaigns pending approval')
                if approvalbutton:
                    jmlhapproval = filter_campaignsdf[filter_campaignsdf['created_by_userid'].isin(approving_list)]
            
        filter_campaigns = filter_campaignsdf[['campaign_id', 'created_by_username', 'campaign_name', 'start_date', 'end_date','approval','notes']]
        if campaign_status=='rejected':
            filter_campaigns=filter_campaigns[['campaign_id', 'created_by_username', 'campaign_name', 'start_date', 'end_date','approval','notes']]
        else:
            filter_campaigns=filter_campaigns[['campaign_id', 'created_by_username', 'campaign_name', 'start_date', 'end_date','approval']]
  
        # Pagination
        page_size = 10
        total_items = len(filter_campaignsdf)
        total_pages = (total_items // page_size)  
        
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = 1

        def change_page(page):
            st.session_state['current_page'] = page    
        
        current_page = st.session_state['current_page']
        start_idx = (current_page - 1) * page_size
        end_idx = start_idx + page_size
        filter_campaigns = filter_campaigns.iloc[start_idx:end_idx]
        
        campaign_event = st.dataframe(filter_campaigns,hide_index=True,on_select="rerun",selection_mode="single-row")
        
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
     
        selectmodecampaign = False
        #selection mode for acc
        try:
            indexselectedcampaign=campaign_event['selection']['rows'][0]
            #load items
            selected_campaign_id=filter_campaigns.iloc[indexselectedcampaign]['campaign_id']
            selected1_campaign_event=filter_campaignsdf[filter_campaignsdf['campaign_id']==selected_campaign_id]
            st.subheader(f"{selected1_campaign_event['campaign_name'].item()}")
            
            pdetil=campaignsdf[campaignsdf['campaign_id']==selected_campaign_id]['project_details'].item() 
            st.caption(f'Project Details: {pdetil}')

            #load data here
            selectedbudgetdf=load_all_budget()
            selectedbudgetd=selectedbudgetdf[selectedbudgetdf['campaign_id'] == selected_campaign_id]
            selectedbudgetd=selectedbudgetd[['activity_grouping', 'activity_budget']]

            selectedgoals=load_all_goals()
            selectedgoals=selectedgoals[selectedgoals['campaign_id'] == selected_campaign_id]
            selectedgoals=selectedgoals
            selectedgoals=selectedgoals[['goal','goal_options','value']]
            scol=st.columns([1,1])
            with scol[0]:
                st.write('**budget**')
                st.dataframe(selectedbudgetd,hide_index=True)

                tb=sum(selectedbudgetd['activity_budget'])
                st.caption(f'total budget {format_rupiah(tb)}')

            with scol[1]:
                st.write('**goals**')
                st.dataframe(selectedgoals,hide_index=True)

            if approvalbutton:
                notesdariapproval=st.text_input('Notes(optional)')
            
        except:pass
        
        if approvalbutton:
            acol=st.columns([1,1,5])
            with acol[0]:
                if st.button('approve'):
                    approval=True
                    update_campaign_button_p(selected_campaign_id,notesdariapproval,approval,user_id,name)
                    st.rerun()

            with acol[1]:
                if st.button('reject'):
                    approval=False
                    update_campaign_button_p(selected_campaign_id,notesdariapproval,approval,user_id,name)
                    st.rerun()
    return approvalbutton

    
    