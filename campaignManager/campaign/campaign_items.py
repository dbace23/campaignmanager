import streamlit as st
from datetime import date, timedelta, datetime,time
from campaignManager.utils.utils import *
from campaignManager.query.query import *

def campaign_item(user_id,name,division):
    goal_options = ['BU Target','Buyer Objectives','Behaviour Objectives','L1 Business Objectives','L0 Business Objectives']
    bu_target=['Fresh & Frozen','AG','AK','AB','Personalized (Affinity)','Retails','All','Private Label','New Initiatives']
    buyer_objective=['New Buyer','New Buyer <3x trx','Existing Buyer (M+2)','Dormant Buyer(>M+2)','New to Component/Channel Buyer','New to Category Buyer','New to Campaign Buyer','New to Brand Buyer','New to SKU buyer','All']
    behaviour_objective=['Qty/order driver','Retention Driver','Frequency Driver','Selling Price/Order Driver','Acquisition']
    L1BO=['CVR','AOV','Retention Rate','Order Frequency','Gross Margin']
    L0BO=['Traffic/NB puller','GMV','Order/#buyer','CM','ARPU']
    budget_options=['KOL', 'Event', 'Digital Ads', 'Brand Partnership', 'Social Media', 'Agency','in app promo']
    
    st.subheader('Campaign Summary')

    p1c1, p1c2, p1c3 = st.columns([2, 1,1])

    with p1c1:
        project_name = st.text_input('Project Name', '', max_chars=50, help="Format sebagai berikut").lower()
    with p1c2:
        maxval = date.today() + timedelta(days=30)
        try:
            startDateCampaign, endDateCampaign = st.date_input("Start date - end date campaign", [date.today(), maxval], min_value=date.today(), help="Jika tidak tahu berakhir kapan atau no end date, pilih tanggal yang sama")
        except:
            st.error('Pilih tanggal mulai dan berakhir. Apabila tidak tahu sampai kapan, pilih 31 Desember sebagai tanggal berakhir')
    with p1c3:
        start_time = time(9, 00)  
        end_time = time(9, 00)  
        # Create time input for start and end times
        start_time_input, end_time_input = st.columns(2)
        with start_time_input:
            startTimeKV = st.time_input('Start time', start_time, help="Select the start time")
        with end_time_input:
            endTimeKV = st.time_input('End time', end_time, help="Select the end time")

    p2c1, p2c2 = st.columns([2, 2])
    with p2c1:
        st.subheader('Budget')
        with st.container():
            options = budget_options
            for i, (grouping, budget) in enumerate(zip(st.session_state['activity_groupings'], st.session_state['activity_grouping_budgets'])):
                available_options = [opt for opt in options if opt not in st.session_state['activity_groupings'] or opt == grouping]
                cols = st.columns([2, 1, 1])
                with cols[0]:
                    st.session_state['activity_groupings'][i] = st.selectbox(f'Activity {i + 1}', available_options, index=available_options.index(grouping), key=f'activity_{i}')
                with cols[1]:
                    st.session_state['activity_grouping_budgets'][i] = st.number_input(f'Budget for {grouping}', min_value=0, step=1, value=int(budget), key=f'budget_{i}')
                with cols[2]:
                    st.caption('')
                    st.caption('')
                    if st.button('❌', key=f'delete_activity_{i}'):
                        del st.session_state['activity_groupings'][i]
                        del st.session_state['activity_grouping_budgets'][i]
                        st.rerun()
            
            # Separate input fields for adding a new activity
            cols = st.columns([2, 1, 1])
            available_options = [opt for opt in options if opt not in st.session_state['activity_groupings']]
            with cols[0]:
                new_activity_group = st.selectbox('New Activity', available_options, key='new_activity')
            with cols[1]:
                new_activity_budget = st.number_input(f'Budget for {new_activity_group}', min_value=0, step=1, key='new_budget')
            with cols[2]:
                st.caption('')
                st.caption('')
                if st.button('➕'):
                    st.session_state['activity_groupings'].append(new_activity_group)
                    st.session_state['activity_grouping_budgets'].append(new_activity_budget)
                    st.rerun()
    project_budget = sum(st.session_state['activity_grouping_budgets'])+new_activity_budget
    st.write(f'Proposed Total budget: {format_rupiah(project_budget)}')
    
    with p2c2:
        st.subheader('Goals')
        with st.container():
            for i, (goal, value) in enumerate(zip(st.session_state['goals'], st.session_state['goal_values'])):
                gcols = st.columns([2, 2, 1, 1])
                available_goal_options = [opt for opt in goal_options if opt not in st.session_state['goals'] or opt == goal]
                with gcols[0]:
                    st.session_state['goals'][i] = st.selectbox(f'Goal {i + 1}', available_goal_options, index=available_goal_options.index(goal), key=f'goal_{i}')
                with gcols[1]:
                    if st.session_state['goals'][i] == 'BU Target': goaloption = bu_target
                    elif st.session_state['goals'][i] == 'Buyer Objectives': goaloption = buyer_objective
                    elif st.session_state['goals'][i] == 'Behaviour Objectives': goaloption = behaviour_objective
                    elif st.session_state['goals'][i] == 'L1 Business Objectives': goaloption = L1BO
                    elif st.session_state['goals'][i] == 'L0 Business Objectives': goaloption = L0BO
                    st.session_state['goal_options'][i] = st.selectbox(f'Goal options {i + 1}', goaloption, key=f'goal_options{i}')
                with gcols[2]:
                    st.session_state['goal_values'][i] = st.number_input(f'value', min_value=0, step=1, value=int(value), key=f'goal_value_{i}')
                with gcols[3]:
                    st.caption('')
                    st.caption('')
                    if st.button('❌', key=f'delete_goal_{i}'):
                        del st.session_state['goals'][i]
                        del st.session_state['goal_options'][i]
                        del st.session_state['goal_values'][i]
                        st.rerun()

            cols = st.columns([2, 2, 1, 1])
            available_goal_options = [opt for opt in goal_options if opt not in st.session_state['goals']]
            with cols[0]:
                new_goals = st.selectbox('New Goals', available_goal_options, key='new_goals')
            with cols[1]:
                if new_goals == 'BU Target': newgoaloption = bu_target
                elif new_goals == 'Buyer Objectives': newgoaloption = buyer_objective
                elif new_goals == 'Behaviour Objectives': newgoaloption = behaviour_objective
                elif new_goals == 'L1 Business Objectives': newgoaloption = L1BO
                elif new_goals == 'L0 Business Objectives': newgoaloption = L0BO
                new_goal_options = st.selectbox('Goal options', newgoaloption, key='goal_options_new')
            with cols[2]:
                new_goal_value = st.number_input(f'value', min_value=0, step=1, key='new_goal_value')
            with cols[3]:
                st.caption('')
                st.caption('')
                if st.button('➕', key='add_goals'):
                    st.session_state['goals'].append(new_goals)
                    st.session_state['goal_options'].append(new_goal_options)
                    st.session_state['goal_values'].append(new_goal_value)
                    st.rerun()

    st.markdown('---')
    project_details = st.text_area('Project Details', '', max_chars=200, help="Tuliskan detil dari project ini secara singkat").lower()

    colc = st.columns([1, 1, 10])
    with colc[0]:
        if st.button('Save'):
            try:
                if not project_name:
                    st.error('Campaign name cannot be blank')
                elif not startDateCampaign or not endDateCampaign:
                    st.error('Start and end dates cannot be blank')
                elif not project_details:
                    st.error('Campaign details cannot be blank')
                else: #if no errors then ....
                    todaydate = datetime.now().strftime('%d')
                    campaign_id = str(user_id)+generate_random_alphanumeric(length=4)
                    campaign_data = {
                        "campaign_id": [campaign_id],
                        "campaign_name": [project_name],
                        "start_date": [startDateCampaign],
                        "end_date": [endDateCampaign],
                        "start_time":[start_time],
                        "end_time":[end_time],
                        "campaign_details": [project_details],
                        "campaign_total_budget": [project_budget],
                        "created_by_userid": [user_id],
                        "created_by_username": [name],
                        "project_details":project_details
                    }
                    campaigndf = pd.DataFrame(campaign_data)
                    campaigndf['created_at'] = datetime.now()
                    campaigndf[['approval', 'approved_by_userid', 'approved_by_username','approved_at', 'deleted_by', 'deleted_at', 'edited_by', 'edited_at','notes']] = None
                    campaigndf['approval']=campaigndf['approval'].astype(bool)
                    campaigndf[['approved_by_userid', 'approved_by_username','deleted_by', 'edited_by','notes']]=campaigndf[['approved_by_userid', 'approved_by_username','deleted_by', 'edited_by','notes']].astype(str)
                    campaigndf['approved_at']=pd.to_datetime(campaigndf['approved_at'])
                    campaigndf['edited_at']=pd.to_datetime(campaigndf['edited_at'])

                    # goals_dataframe
                    st.session_state['goals'].append(new_goals)
                    st.session_state['goal_values'].append(new_goal_value)
                    st.session_state['goal_options'].append(new_goal_options)
                    data_goals = {'goal': st.session_state['goals'],'goal_options':st.session_state['goal_options'],'value': st.session_state['goal_values']}
                    goals_df = pd.DataFrame(data_goals)
                    goals_df['campaign_id'] = campaign_id
                    goals_df['created_by_userid'] = [user_id] * len(goals_df)
                    goals_df['created_by_username'] = [name] * len(goals_df)
                    goals_df['created_at'] = [datetime.now()] * len(goals_df)
                    goals_df['level'] = 'campaign'
                    goals_df[['edited_at', 'edited_by', 'activity_id']] = None
                    goals_df['goal_id'] = goals_df.apply(lambda row:str(campaign_id)+"_"+generate_random_alphanumeric(length=4), axis=1)
    
                    # budget_dataframe
                    st.session_state['activity_groupings'].append(new_activity_group)
                    st.session_state['activity_grouping_budgets'].append(new_activity_budget)
                    data_activity = {'activity_grouping': st.session_state['activity_groupings'], 'activity_budget': st.session_state['activity_grouping_budgets']}
                    activity_df = pd.DataFrame(data_activity)
                    activity_df['campaign_id'] = campaign_id
                    activity_df['created_by_userid'] = [user_id] * len(activity_df)
                    activity_df['created_by_username'] = [name] * len(activity_df)
                    activity_df['created_at'] = [datetime.now()] * len(activity_df)
                    activity_df['level'] = 'campaign'
                    activity_df[['edited_at', 'edited_by', 'activity_id']] = None
                    activity_df['goal_id'] = activity_df.apply(lambda row: str(campaign_id)+"_"+generate_random_alphanumeric(length=4), axis=1)
 
                    save_campaign(campaigndf, goals_df, activity_df)
                    clear_goals()
                    clear_budgets()

                    st.session_state['main_page'] = 'Campaigns'
                    st.rerun()
            except Exception as saveE:
                with colc[2]:
                    st.error(f'error {saveE}')
    
    with colc[1]:
        if st.button('Cancel'):
            st.session_state['main_page'] = 'Campaigns'
            clear_goals()
            clear_budgets()
            st.rerun()

    return project_name, startDateCampaign, endDateCampaign, project_details, project_budget
