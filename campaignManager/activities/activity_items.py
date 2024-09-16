import streamlit as st
import uuid
from datetime import time
from datetime import date, timedelta, datetime
from campaignManager.utils.utils import *
from campaignManager.query.query import *

def utmplus(utmid,alias, placement, destination, destinationurl, destinationapp, finaldeeplinkValue, bu, deeplinkid):
    st.caption('')
    st.caption('')
    if st.button('➕', key='plusUTM'):
        st.session_state['utm_data'].append({
            'utmid':utmid,
            'alias': alias,
            'placement': placement, 
            'destination': destination,
            'destination_url': destinationurl, 
            'destination_app': destinationapp,
            'final_deeplink_value': finaldeeplinkValue, 
            'bu': bu,
            'deeplink_id': deeplinkid
        })
        st.rerun()

def delutm(colau, nx, idx):
    with colau[nx]:
        st.caption('')
        st.caption('')
        if st.button('❌', key=f'delete_utm_{idx}'):
            del st.session_state['utm_data'][idx]
            st.rerun()
            
def activityitem(user_id,name,division,campaigns,approvedbudget,approvedgoals):

    utmdf=pd.DataFrame()
    kvdf=pd.DataFrame()
    promodf=pd.DataFrame()

    st.subheader('Activity Creator')
  
    #
    goal_options = ['BU Target','Buyer Objectives','Behaviour Objectives','L1 Business Objectives','L0 Business Objectives']
    bu_target=['Fresh & Frozen','AG','AK','AB','Personalized (Affinity)','Retails','All','Private Label','New Initiatives']
    buyer_objective=['New Buyer','New Buyer <3x trx','Existing Buyer (M+2)','Dormant Buyer(>M+2)','New to Component/Channel Buyer','New to Category Buyer','New to Campaign Buyer','New to Brand Buyer','New to SKU buyer','All']
    behaviour_objective=['Qty/order driver','Retention Driver','Frequency Driver','Selling Price/Order Driver','Acquisition']
    L1BO=['CVR','AOV','Retention Rate','Order Frequency','Gross Margin']
    L0BO=['Traffic/NB puller','GMV','Order/#buyer','CM','ARPU']

    #
    jeniskegiatan=['KOL', 'Offline Event', 'Digital Ads', 'Brand Partnership', 'Social Media', 'Agency','SEO','inapp promotion','others']
    koltype=['nano', 'micro', 'macro']
    activitytype=['community', 'O2O', 'goes to campus', 'residence', 'event Tap In']
    adplatformtype=['meta', 'google', 'tiktok', 'x']
    brandtype=['co-marketing', 'co-branding', 'sponsorship']
    sosmedtype=['instagram','tiktok','x','facebok','linkedin']
    agencytype=['PPC advertising agency', 'social media agency', 'SEO agency', 'inffluencer marketing agency', 'email marketing agency']
    seotype=['site','blog','backlinks']

    metaobj=['brand awareness', 'reach', 'traffic', 'engagement', 'app installs', 'video views', 'lead generation', 'messages', 'conversions', 'catalog sales', 'store traffic', 'event responses', 'offer claims']
    googleob=['sales','leads','website traffic','product & brand consideration','brand awareness and reach','app promotion','local store visits and promotion','no guidance']
    tiktokobj=['reach','traffic','app installs','video views','lead generation','conversions','catalog sales']
    xobj=['reach, tweet engagement, video views, app installs followers, app re engagement']

    social_media_placement=['instagram story', 'instagram reels', 'instagram feed', 'instagram live', 'instagram broascast', 'facebook feed', 'facebook stories', 'facebook reels', 'x', 'linkedin story', 'whatsapp story', 'whatsapp blast', "website", 'youtube', 'tiktok']


    campaigns['campaign_id_name'] = campaigns['campaign_id'] + "_" + campaigns['campaign_name']
    campaign_names = campaigns['campaign_id_name'].unique()

##############################################    #logic
    if len(campaign_names)>0: #check if there's approved items
        selected_campaign = st.selectbox('Choose Campaign Umbrella', campaign_names)
        selected_campaign_id=selected_campaign.split("_")[0]
        
        #load approved kegiatan
        updated_kegiatan_options = []
        for keg in jeniskegiatan:
            if keg in approvedbudget['activity_grouping'].values:
                updated_kegiatan_options.append(keg+'- planned')
            else:
                updated_kegiatan_options.append(keg)
        jeniskegiatan=updated_kegiatan_options

        #helper for budget brpa
        groupedbud = approvedbudget.groupby(['activity_grouping', 'level']).agg({'activity_budget': 'sum'}).reset_index()
        pivotedbud = groupedbud.pivot_table(index=['activity_grouping'],
                                    columns='level',
                                    values='activity_budget',
                                    aggfunc='sum',
                                    fill_value=0).reset_index()
        if 'activity' not in pivotedbud.columns:  
            pivotedbud['activity'] = 0
        pivotedbud['difference'] = pivotedbud['campaign'] - pivotedbud['activity']

        #load approved goals
        campgoals=approvedgoals[approvedgoals['campaign_id']==selected_campaign_id]
        updated_goal_options = []
        for goal in goal_options:
            if goal in approvedgoals['goal'].values:  # Check if goal is not in the 'goals' column
                updated_goal_options.append(goal + '- planned')  # Append "-planned" if not found
            else:
                updated_goal_options.append(goal)  # Keep the goal as is if found
        # Update the goal_options with the new values
        goal_options = updated_goal_options

        #if want to fill only goals set by campaign 
        # grouped = campgoals.groupby(['goal', 'goal_options', 'level']).agg({'value': 'sum'}).reset_index()
        # # Pivot the table to have separate columns for campaign and activity sums
        # pivoted = grouped.pivot_table(index=['goal', 'goal_options'],
        #                             columns='level',
        #                             values='value',
        #                             aggfunc='sum',
        #                             fill_value=0).reset_index()
        # if 'activity' not in pivoted.columns:  
        #     pivoted['activity'] = 0
        # pivoted['difference'] = pivoted['campaign'] - pivoted['activity']
        # st.session_state['goals'] = pivoted['goal'].tolist()  # Convert column to list and store in session state
        # st.session_state['goal_options'] = pivoted['goal_options'].tolist()  # Convert column to list and store in session state
        # st.session_state['goal_values'] = pivoted['difference'].tolist() 
 
        #load activity


        h1c1, h1c2 = st.columns([1, 2])
        with h1c1:
            st.subheader('Activity Details')
        with h1c2:
            st.subheader('goals')
        a1c1, a1c2 = st.columns([1, 2])
        with a1c1:
            activity_grouping_sel = st.selectbox('pilih jenis kegiatan',  jeniskegiatan)
            activity_grouping=activity_grouping_sel.split("-")[0]
            if activity_grouping=='KOL':activity_name=st.selectbox('choose KOL type', koltype,help='nano<10,000, micro=10,000-100,000, macro>10,000')
            if activity_grouping=='Offline Event':activity_name=st.selectbox('choose activity',  activitytype)
            if activity_grouping=='Digital Ads':activity_name=st.selectbox('choose platform', adplatformtype)
            if activity_grouping=='Brand Partnership':activity_name=st.selectbox('choose activity', brandtype)
            if activity_grouping=='Social Media':activity_name=st.selectbox('choose platform', sosmedtype)
            if activity_grouping=='Agency':activity_name=st.selectbox('choose agency type', agencytype)
            if activity_grouping=='SEO':activity_name=st.selectbox('choose seo type', seotype)
            if activity_grouping=='others':
                activity_name=st.text_input('activity name', max_chars=50, help=f"harap diisi").lower()
                activity_details=st.text_input(f'activity grouping', max_chars=50, help=f"harap diisi").lower()
            
            if activity_grouping not in ('Digital Ads','Social Media','others'):
                if activity_grouping == 'KOL':activity_name = 'KOL name'
                if activity_grouping=='Agency':activity_name='Agency Name'
                if activity_grouping=='Brand Partnership':activity_name='Brand Name'
                if activity_grouping=='Offline Event':activity_name=f'{activity_name} Name'
                if activity_grouping=='SEO':activity_name=f'{activity_name} content'
                activity_details = st.text_input(f'{activity_name}', max_chars=50, help=f"harap diisi").lower()
            if activity_grouping=='Digital Ads':
                if activity_name=='meta':obj=metaobj
                if activity_name=='google':obj=googleob
                if activity_name=='tiktok':obj=tiktokobj
                if activity_name=='x':obj=xobj
                activity_details=st.selectbox('choose objective', obj)
            if activity_grouping=='Social Media':
                sosmed_placement=[item for item in social_media_placement if activity_name in item] 
                activity_details=st.selectbox('choose placement',sosmed_placement)

            sdate = campaigns[campaigns['campaign_id'] == selected_campaign_id]['start_date'].item()
            edate = campaigns[campaigns['campaign_id'] == selected_campaign_id]['end_date'].item()
            if isinstance(sdate, str):
                sdate = datetime.strptime(sdate, "%Y-%m-%d").date()  # Convert from string to date
            elif isinstance(sdate, pd.Timestamp):
                sdate = sdate.date()  
            if isinstance(edate, str):
                edate = datetime.strptime(edate, "%Y-%m-%d").date()  # Convert from string to date
            elif isinstance(edate, pd.Timestamp):
                edate = edate.date()  # Convert from Timestamp to date
            # Set maxval and minval based on the dates
            maxval = edate
            if sdate>date.today():
                minval=sdate
            else:minval=date.today()
            try:
                startDateActivity, endDateActivity = st.date_input("Start date - end date activity", [minval, maxval], min_value=date.today(), help="wajib end date",key='activitydate')
            except:
                st.error('Pilih tanggal mulai dan berakhir. ')

            start_time = time(9, 00)  
            end_time = time(9, 00)  
            # Create time input for start and end times
            start_time_input, end_time_input = st.columns(2)
            with start_time_input:
                startTimeKV = st.time_input('Start time', start_time, help="Select the start time",key='activitytime')
            with end_time_input:
                endTimeKV = st.time_input('End time', end_time, help="Select the end time",key='activitytime2')

            #activity budget
            if "-" in activity_grouping_sel:
                abduit=pivotedbud[pivotedbud['activity_grouping']==activity_grouping]['difference'].item()
            else:
                abduit=0

            activity_budget = st.number_input('activity Budget', min_value=abduit, step=1, help="Masukkan anggaran dalam Rp.")
  
            if "-" not in activity_grouping_sel:
                st.error('aktifitas diluar persetujuan campaign eror')
        with a1c2:
            with st.container():
                for i, (goal, value) in enumerate(zip(st.session_state['goals'], st.session_state['goal_values'])):
                    gcols = st.columns([2, 2, 1, 1])
                    available_goal_options = [opt for opt in goal_options if opt not in st.session_state['goals'] or opt == goal]
                    with gcols[0]:
                        st.session_state['goals'][i] = st.selectbox(f'Goal {i + 1}', available_goal_options, index=available_goal_options.index(goal), key=f'goal_{i}')
                    with gcols[1]:
                        if st.session_state['goals'][i] == 'BU Target':
                            goaloption = bu_target
                        elif st.session_state['goals'][i] == 'Buyer Objectives':
                            goaloption = buyer_objective
                        elif st.session_state['goals'][i] == 'Behaviour Objectives':
                            goaloption = behaviour_objective
                        elif st.session_state['goals'][i] == 'L1 Business Objectives':
                            goaloption = L1BO
                        elif st.session_state['goals'][i] == 'L0 Business Objectives':
                            goaloption = L0BO
                        st.session_state['goal_options'][i] = st.selectbox(f'Goal options {i + 1}', goaloption, key=f'goal_options{i}')
                    with gcols[2]:
                        st.session_state['goal_values'][i] = st.number_input(f'Value', min_value=0, step=1, value=int(value), key=f'goal_value_{i}')
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
                    new_goals=new_goals.split("-")[0]
                with cols[1]:
                    if new_goals == 'BU Target':
                        newgoaloption = bu_target
                    elif new_goals == 'Buyer Objectives':
                        newgoaloption = buyer_objective
                    elif new_goals == 'Behaviour Objectives':
                        newgoaloption = behaviour_objective
                    elif new_goals == 'L1 Business Objectives':
                        newgoaloption = L1BO
                    elif new_goals == 'L0 Business Objectives':
                        newgoaloption = L0BO
                    new_goal_options = st.selectbox('Goal options', newgoaloption, key='goal_options_new')
                with cols[2]:
                    new_goal_value = st.number_input(f'Value', min_value=0, step=1, key='new_goal_value')
                with cols[3]:
                    st.caption('')
                    st.caption('')
                    if st.button('➕', key='add_goals'):
                        st.session_state['goals'].append(new_goals)
                        st.session_state['goal_options'].append(new_goal_options)
                        st.session_state['goal_values'].append(new_goal_value)
                        st.rerun()
 
    # UTM segment
    st.markdown("---")
    
    if len(st.session_state['utm_data']) <= 0:
        if st.button('➕ UTM'):
            new_utmid = str(uuid.uuid4())[:5]
            st.session_state['utm_data'].append({'utmid':new_utmid,'alias': '', 'placement': '', 'destination': '', 'destination_url': '', 'destination_app': '', 'final_deeplink_value': '', 'bu': '', 'deeplink_id': ''})
            st.rerun()
    else:
        st.subheader('UTM')

    for idx, utm in enumerate(st.session_state['utm_data']):
        colau = st.columns([3, 3, 2, 3, 3, 2, 1, 1])
        with colau[0]:
            st.session_state['utm_data'][idx]['alias'] = st.text_input(f'Alias', value=utm['alias'], key=f'alias{idx}')
        with colau[1]:
            social_media_placement = ('instagram story', 'instagram reels', 'instagram feed', 'instagram live', 'instagram broascast', 'facebook feed', 'facebook stories', 'facebook reels', 'x', 'linkedin story', 'whatsapp story', 'whatsapp blast', "website", 'youtube', 'tiktok')
            offline_placement = ('whatsapp', 'poster', 'banner', 'billboard', 'flyer', 'newspaper', 'magazine', 'lift poster', 'email', 'print coupon', 'newsletter', 'product packaging', 'pos display', 'calendar', 'shirt', 'astro website', 'astro app banner')
            ads_placement = ('google', 'meta', 'tiktok', 'linkedin', 'x')
            if activity_grouping == 'KOL':
                placement = social_media_placement
            elif activity_grouping == 'Offline Event':
                placement = offline_placement
            elif activity_grouping == 'Digital Ads':
                placement = [(activity_name)]
            elif activity_grouping == 'Brand Partnership':
                placement = social_media_placement + ads_placement + offline_placement
            elif activity_grouping == 'Social Media':
                placement = [(activity_details)]
            elif activity_grouping == 'Agency':
                placement =  [(activity_details)]
            elif activity_grouping == 'SEO':
                placement = [(activity_name)]
            elif activity_grouping == 'others':
                placement = []
            st.session_state['utm_data'][idx]['placement'] = st.selectbox(f'Pilih penempatan UTM', tuple(list(sorted(placement)) + ['others']), key=f'placement_type{idx}')
            if st.session_state['utm_data'][idx]['placement'] == 'others':
                with colau[2]:
                    st.session_state['utm_data'][idx]['placement'] = st.text_input(f'Other placement', 'new placement', key=f'placement{idx}')
                    n = 1
            else:
                n = 0
        with colau[2 + n]:
            st.session_state['utm_data'][idx]['destination'] = st.selectbox(f'Pilih destination', ('web', 'app'), key=f'destination{idx}')
        with colau[3 + n]:
            if st.session_state['utm_data'][idx]['destination'] == 'web':
                st.session_state['utm_data'][idx]['destination_url'] = st.text_input(f'Enter URL', key=f'destination_url{idx}')
                if len(st.session_state['utm_data']) == idx + 1:
                    with colau[4 + n + 1]:
                        if activity_grouping!='Social Media':
                            utmplus(generate_random_alphanumeric(length=4),st.session_state['utm_data'][idx]['alias'], st.session_state['utm_data'][idx]['placement'], st.session_state['utm_data'][idx]['destination'], st.session_state['utm_data'][idx]['destination_url'], None, None, None, None)
                        delutm(colau, 4 + n, idx)
                else:
                    delutm(colau, 4 + n, idx)
            if st.session_state['utm_data'][idx]['destination'] == 'app':
                st.session_state['utm_data'][idx]['destination_app'] = st.selectbox(f'Pilih destination app', ('home', 'product-detail', 'catalog', 'category', 'custom'), key=f'destination_app{idx}')
                with colau[4 + n]:
                    if st.session_state['utm_data'][idx]['destination_app'] == 'custom':
                        st.session_state['utm_data'][idx]['final_deeplink_value'] = st.text_input(f'Deeplink path', key=f'final_deeplink{idx}')
                        if len(st.session_state['utm_data']) == idx + 1:
                            with colau[5 + n + 1]:
                                if activity_grouping!='Social Media':
                                    utmplus(generate_random_alphanumeric(length=4),st.session_state['utm_data'][idx]['alias'], st.session_state['utm_data'][idx]['placement'], st.session_state['utm_data'][idx]['destination'], st.session_state['utm_data'][idx]['destination_url'], st.session_state['utm_data'][idx]['destination_app'], st.session_state['utm_data'][idx]['final_deeplink_value'], None, None)
                                delutm(colau, 5 + n, idx)
                        else:
                            delutm(colau, 5 + n, idx)
                    else:
                        st.session_state['utm_data'][idx]['bu'] = st.selectbox(f'Business unit', ('instant', 'super'), key=f'bu{idx}')
                        if st.session_state['utm_data'][idx]['destination_app'] != 'home':
                            with colau[5 + n]:
                                st.session_state['utm_data'][idx]['deeplink_id'] = st.text_input(f'Id value', key=f'deeplink{idx}')
                                st.session_state['utm_data'][idx]['final_deeplink_value'] = f'astro//{st.session_state["utm_data"][idx]["destination_app"]}/{st.session_state["utm_data"][idx]["deeplink_id"]}'
                                if len(st.session_state['utm_data']) == idx + 1:
                                    with colau[6 + n + 1]:
                                        utmplus(generate_random_alphanumeric(length=4),st.session_state['utm_data'][idx]['alias'], st.session_state['utm_data'][idx]['placement'], st.session_state['utm_data'][idx]['destination'], st.session_state['utm_data'][idx]['destination_url'], st.session_state['utm_data'][idx]['destination_app'], st.session_state['utm_data'][idx]['final_deeplink_value'], st.session_state['utm_data'][idx]['bu'], st.session_state['utm_data'][idx]['deeplink_id'])
                                        delutm(colau, 6 + n, idx)
                                else:
                                    delutm(colau, 6 + n, idx)
                                if st.session_state['utm_data'][idx]['bu'] == 'super':
                                    st.session_state['utm_data'][idx]['final_deeplink_value'] = f'{st.session_state["utm_data"][idx]["final_deeplink_value"]}?deliveryType=super'
                        else:
                            if len(st.session_state['utm_data']) == idx + 1:
                                with colau[5 + n + 1]:
                                    utmplus(generate_random_alphanumeric(length=4),st.session_state['utm_data'][idx]['alias'], st.session_state['utm_data'][idx]['placement'], st.session_state['utm_data'][idx]['destination'], st.session_state['utm_data'][idx]['destination_url'], st.session_state['utm_data'][idx]['destination_app'], st.session_state['utm_data'][idx]['final_deeplink_value'], st.session_state['utm_data'][idx]['bu'], st.session_state['utm_data'][idx]['deeplink_id'])
                                    delutm(colau, 5 + n, idx)
                            else:
                                delutm(colau, 5 + n, idx)
                            st.session_state['utm_data'][idx]['final_deeplink_value'] = 'astro//home'
    if len(st.session_state['utm_data']) > 0:
        utmdata = st.session_state['utm_data']
        utmdf = pd.DataFrame(utmdata)
        utmdf['campaign_id'] = selected_campaign_id
        utmdf['created_by_userid'] = user_id
        utmdf['created_by_username'] = name
        utmdf['created_at'] = datetime.now()
        utmdf[['edited_at', 'edited_by']] = None
        utmdf['medium']=activity_grouping
    
    # digital ads segment
    if activity_grouping=='Digital Ads':
    
        cname=selected_campaign.split("_")[1]
        cid=selected_campaign.split("_")[0]
     
        campaign_level_naming=cid+"_"+name+"_"+str(startDateActivity).replace("-","")+"_"+cname
        ad_group_naming="audience/keywordGroupingTarget"
        ad_naming="kvName"+"_"+'kvId'
        if len(utmdf)>0:
            st.markdown("---")
            st.markdown(f"**Digital Ads Naming**") 

            adcampaign_list = []
            adgroupname_list = []
            adname_list = []
    
            for i in range(len(utmdf)):
                
                dacols = st.columns([1, 1, 1])
                with dacols[0]:
                    campaign_level_naming = cid + "_" + name + "_" + str(startDateActivity).replace("-", "") + "_" + cname
                    adcampaign = st.text_input(f'Suggested campaign name {i + 1}', campaign_level_naming, key=f'adcampaign_{i}')
                    adcampaign_list.append(adcampaign)  # Append each ad campaign name
                with dacols[1]:
                    ad_group_naming = "audience/keywordGroupingTarget"
                    adgroupname = st.text_input(f'Ad group/set name {i + 1}', ad_group_naming, key=f'adgroupname_{i}')
                    adgroupname_list.append(adgroupname)  # Append each ad group name
                with dacols[2]:
                    ad_naming = "ganti ini"+"|"+utmdf['utmid'][i]
                    adname = st.text_input(f'Ad name {i + 1}', ad_naming, key=f'adname_{i}')
                    adname_list.append(adname)  # Append each ad name
          
            # Now replicate the adcampaign, adgroupname, and adname columns in the dataframe
            utmdf['adcampaign'] = adcampaign_list
            utmdf['adgroupname'] = adgroupname_list
            utmdf['adname'] = adname_list
  
        else:
            st.write('Make utm to create ad names')
    else:
        utmdf['adcampaign'] = None
        utmdf['adgroupname'] = None
        utmdf['adname'] = None
################################################################################# PROMO
    st.markdown("---")
    if st.session_state['empty_state_voucher']:
        if st.button('➕ PROMO'):
            st.session_state['empty_state_voucher'] = False
            st.rerun()
    else:
        st.subheader('Promo')
        #load saved promo
        try:
            if len(st.session_state['voucher_data'])>0:
        
                tempdatdf=pd.DataFrame(st.session_state['voucher_data'])
                tempdatdf['unique_name']=tempdatdf['promo_id']+"_"+tempdatdf['promo_code_name']
                ext_promo=tempdatdf['unique_name'].unique()
                pilihanpromo=['saved','new','none']
            else:pilihanpromo=['new','none']
        except:pilihanpromo=['new','none']

  
        promolistselected=[]
        promcols= st.columns([1,2,1])
        if activity_grouping=='Digital Ads':
            if len(utmdf)>0:
                for i in range(len(utmdf)):
                    with promcols[0]:
                        if i==0:isipromo=pilihanpromo
                        else:isipromo=pilihanpromo
                        promo_type_=st.selectbox(f'promo type{i+1}', isipromo, key=f'promo type_{i}')  
                    if promo_type_=='saved':
                        with promcols[1]:
                            promoselected=st.selectbox(f'saved promo{i+1}', ext_promo+"_"+utmdf['utmid'][i], key=f'promo type_selection{i}')
                            promolistselected.append(promoselected)
                    elif promo_type_=='none':
                        with promcols[1]:
                            blank=st.text_input(f' ', key=f'blank',disabled=True)
                      
        else:
            with promcols[0]:
                promo_type_=st.selectbox('promo type', pilihanpromo, key='promo type_')  
            if promo_type_=='saved':
                with promcols[1]:
                    promoselected=st.selectbox('saved promo', ext_promo, key='promo type_selection')
                    promolistselected.append(promoselected)
        try:
            if promo_type_=='new':
                st.markdown(f"**PROMO CREATOR**") 
        
                with st.container():
                    vcols = st.columns([1, 1, 1])
                    with vcols[0]:
                        promo_l0=st.selectbox('L0 promo', ('voucher', 'discount', 'bmsm','PWP','GWP','VB','reff. code(U2U)','reff. code(KOL2U)'), key='L0promo')

                        if promo_l0=='voucher':
                            alias = st.text_input('promo code', key='alias', max_chars=20)
                        else:
                            alias = st.text_input('promo name', key='alias', max_chars=20)   

                        if promo_l0=='voucher':
                            pilipromol1=('free delivery', 'price cut')
                        else:
                            pilipromol1=[('others')]    
                        promo_l1=st.selectbox('L1 promo', pilipromol1, key='L1promo')

                        maxval = date.today() + timedelta(days=30)
                        start_date, end_date = st.date_input("Start date-end date", [date.today(), maxval], min_value=date.today(), key='date_range')


                        product_target = st.selectbox('Target Product', ('products', 'l1_category', 'all sku', 'ak', 'ag', 'ab'), key='product_target')
                    with vcols[1]:
                        
                        quota_type = st.selectbox('Quota Type', ('daily', 'lifetime'), key='quota_type')

                        max_benefit = st.number_input('Max Benefit (Rp)', min_value=0, step=1, key='Max_Benefit')

                        min_transaction = st.number_input('Min Transaction(Rp)', min_value=0, step=1, key='Min_Transaction')

                        perc_benefit = st.number_input('Percentage Benefit', min_value=0, step=1, key='perc_Benefit')
                        
                        product_target_value = st.text_input('Temporary Holder For product.category id', key='product_target_value')
                    with vcols[2]:
                       

                        quota_value = st.number_input('Quota Value', min_value=0, step=1, key='quota_value')

                        opb = st.number_input('order per buyer', min_value=0, step=1, key='opb')

                        perc_partner_budget = st.number_input('Percentage Partner Budget', min_value=0, step=1, key='perc_Partner_Budget')

                        if perc_partner_budget > 0:
                            SKP_Number = st.text_input('SKP Number', key='SKP_Number')
                        else:
                            SKP_Number = ""
    
                        
                tnc = st.text_area('T&C', key='tnc')

                if quota_type == 'lifetime':
                    total_expense = max_benefit * quota_value
                else:
                    total_days = (end_date - start_date).days
                    total_expense = max_benefit * quota_value * total_days

                st.write(f'Total Expense: {format_rupiah(total_expense)}')

                with st.container():
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button('Save', key='save promo'):
                            st.session_state['voucher_data'].append({
                                'promo_id':promo_l0[:2]+str(date.today().day)+generate_random_alphanumeric(length=4),
                                'promo_L0': promo_l0,
                                'promo_l1': promo_l1,
                                'start_date': start_date,
                                'promo_code_name':alias,
                                'end_date': end_date,
                                'quota_type': quota_type,
                                'quota_value': quota_value,
                                'perc_benefit': perc_benefit,
                                'max_benefit': max_benefit,
                                'order_per_buyer':opb,
                                'min_transaction': min_transaction,
                                'partner_budget': perc_partner_budget,
                                'SKP_Number': SKP_Number,
                                'product_target': product_target,
                                'product_target_value': product_target_value,
                                'tnc': tnc,
                                'total_expense': total_expense
                            })
                            st.rerun()
        except Exception as e:
            st.error(f'create utm to get promo {e}')
        with promcols[2]:
            st.caption('')
            st.caption('')
            if st.button('❌', key=f'delete_promo'):
                del st.session_state['voucher_data']
                st.session_state['empty_state_voucher'] = True
                st.rerun()


    #Slot Request
    st.markdown("---")
    st.subheader('Slot')
    ext_kv=pd.read_csv('campaigns.csv')
    ext_kv=ext_kv.campaign_name.unique()
    #load existing promo
    kv_type_=st.selectbox('kv type', ('new','existing'), key='kv type_')
    if kv_type_=='existing':
        st.selectbox('current kv', ext_promo, key='kv type_selection')
    elif kv_type_=='new':
        if st.session_state['empty_state_kv']:
            if st.button('➕ KV'):
                st.session_state['empty_state_kv'] = False

    if not st.session_state['empty_state_kv']:
        st.subheader('Slot Request')
        with st.container():
            vcols = st.columns([1, 1, 1,1])
            with vcols[0]:
                kv_name=st.text_input('slot name')
                kv_type=st.selectbox('KV type', ('dedicated HPB','Mixed HPB','Catalog Tile','2x2 Banner','Pop Up Banner'), key='kv_type')
                if kv_type=='Catalog Tile':
                    kv_asset_remarks=st.text_input('KV asset type remarks', key='kv remarks')
                kv_slot=st.number_input(f'KV slot rank', min_value=0, step=1, value=int(1), key=f'kv_value')
          
            with vcols[1]:
                startDateKV, endDateKV = st.date_input("Start date - end date", [date.today(), maxval], min_value=date.today(), help="wajib ada end date")
                start_time = time(9, 00)  
                end_time = time(17, 00)  
                # Create time input for start and end times
                start_time_input, end_time_input = st.columns(2)
                with start_time_input:
                    startTimeKV = st.time_input('Start time', start_time, help="Select the start time")
                with end_time_input:
                    endTimeKV = st.time_input('End time', end_time, help="Select the end time")

                kv_type2=st.selectbox('KV type2', ('ad hoc','BAU','Habitual','Mega'), key='kv_type2')          

            with vcols[2]:
                kv_maxdisc=st.number_input(f'max discount', min_value=0, step=1, value=int(1), key=f'kv_maxdiscount')
                kv_disctype=st.selectbox('disc type', ('percentage','price point','USP','harga coret'), key='kv_disctype')  
                kv_copy=st.text_input('marketing copy', key='kv_marketingcopy')  
                kv_secValue=st.selectbox('2nd value prop', ('flash sale','free ongkir','free gift','voucher','none'), key='kv_sevalue')  
 
        with st.container():
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button('Save', key='save kv'):
                    st.session_state['kv_data'].append({
                        'kvid':'kv'+str(date.today().day)+generate_random_alphanumeric(length=4),
                        'kv_name':kv_name,
                        'kv_type':kv_type,
    
                    })
                    st.session_state['empty_state_kv'] = True
                    st.rerun()
 

    try:
        if len(st.session_state['kv_data']) > 0:
            st.subheader('KV LIST')
            with st.container():
                for nutm, vouch in enumerate(st.session_state['kv_data']):
                    vcols = st.columns([1,1,1, 1, 1, 1, 1])
                    with vcols[0]:
                        st.text_input('kvid', value=vouch['kvid'], key=f'kvid{nutm}', disabled=True)
                    with vcols[1]:
                        st.text_input('kv name', value=vouch['kv_name'], key=f'kv_name{nutm}', disabled=True)
                    with vcols[2]:
                        st.text_input('kv_type', value=vouch['kv_type'], key=f'kv_type{nutm}', disabled=True)
                    with vcols[3]:
                        st.text_input('aspect ratio', value=vouch['aspect_ratio'], key=f'aspectratio{nutm}', disabled=True)
      
            
            kvdf=pd.DataFrame(st.session_state['kv_data'])
    except Exception as e:
        st.error(e)

    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button('Save Activity'):
            if not activity_name:
                st.error('activity_name cannot be blank')
            elif not startDateActivity or not endDateActivity:
                st.error('Start and end dates cannot be blank')
            else:
                tdid=datetime.now().strftime("%Y%m%d")[2:]
                activity_id=tdid+generate_random_alphanumeric(length=4)
                #activitydf
                activity_dat={
                'campaign_id':selected_campaign_id,
                'activity_id':activity_id,
                'activity_grouping':activity_grouping,
                'activity_name':activity_name,
                'activity_details':activity_details,
                'start_date':startDateActivity, 
                'end_date':endDateActivity,
                'start_time':start_time,
                'end_time':end_time,
                'estimated_budget':activity_budget,
                'created_by_userid':user_id,
                'created_by_username':name,
                'created_at':datetime.now()
                }
                activitydf=pd.DataFrame([activity_dat])
                activitydf[['approval', 'approved_by_userid','approved_by_username','approved_at', 'deleted_by', 'deleted_at', 'edited_by', 'edited_at','notes']] = None

                #goalsdf
                st.session_state['goals'].append(new_goals)
                st.session_state['goal_values'].append(new_goal_value)
                st.session_state['goal_options'].append(new_goal_options)
                data_goals = {'goal': st.session_state['goals'],'goal_options':st.session_state['goal_options'],'value': st.session_state['goal_values']}
                goals_df = pd.DataFrame(data_goals)
                goals_df['campaign_id'] = selected_campaign_id
                goals_df['activity_id']=activity_id
                goals_df['created_by_userid'] = [user_id] * len(goals_df)
                goals_df['created_by_username'] = [name] * len(goals_df)
                goals_df['created_at'] = [datetime.now()] * len(goals_df)
                goals_df['level'] = 'activity'
                goals_df[['edited_at', 'edited_by']] = None
                goals_df['goal_id'] = goals_df.apply(lambda row:str(selected_campaign_id)+"_"+tdid+generate_random_alphanumeric(length=4), axis=1)

                if len(st.session_state['utm_data']) > 0:
                    #utm
                    utmdf['activity_id']=activity_id
                    utmdf['url']=""
                    utmdf[['edited_at', 'edited_by']] = None
                else:
                    utmdf=pd.DataFrame()

                if st.session_state['empty_state_voucher'] == False:
                    if len(promolistselected)>0:
                        if activity_grouping=='Digital Ads':
                            helperdf = pd.DataFrame([item.split('_') for item in promolistselected], columns=['promo_id', 'promoname', 'utmid'])
                        else:
                            helperdf = pd.DataFrame([item.split('_') for item in promolistselected], columns=['promo_id', 'promoname'])
                    
                        #promo
                        promodf= tempdatdf[tempdatdf['promo_id'].isin(helperdf['promo_id'].unique())]
                        promodf['created_by']=user_id
                        promodf['created_at']=datetime.now()
                        promodf['campaign_id'] = selected_campaign_id
                        promodf['activity_id']=activity_id
                        promodf[['edited_at', 'edited_by','approved']] = None

                        #addeditemsutm
                        if len(st.session_state['utm_data']) > 0:
                            if activity_grouping=='Digital Ads':
                                utmdf=pd.merge(utmdf,helperdf[['utmid', 'promo_id']],on='utmid', how='left')
                            else:
                                promoids=promodf['promo_id'].unique().item()
                                utmdf['promo_id']=promoids 

                    else:
                        promodf=pd.DataFrame()
                        utmdf['promo_id']=None
                else:promodf=pd.DataFrame()
                kvdf=pd.DataFrame()
                #kv
                # kvdf['kv_id']=kvdf.apply(lambda row: "kv"+generate_random_alphanumeric(length=5), axis=1)
                # kvdf['created_by']=user_id
                # kvdf['created_at']=datetime.now()
                # kvdf['campaign_id'] = campaign_id_sel
                # kvdf['activity_id']=activity_id
                # kvdf[['edited_at', 'edited_by']] = None

                #clear session
                st.session_state['utm_data']=[]
                st.session_state['voucher_data']=[]
                st.session_state['kv_data']=[]
                clear_goals()
                clear_budgets()
                save_activity(activitydf,goals_df,utmdf,promodf,kvdf)
                st.session_state['main_page'] = 'Activities'
                st.rerun()
    with col2:
        if st.button('Cancel  Activity'):
            #clear session
            st.session_state['utm_data']=[]
            st.session_state['voucher_data']=[]
            st.session_state['kv_data']=[]
            clear_goals()
            clear_budgets()
            st.session_state['main_page'] = 'Activities'
            st.rerun()
 

 
