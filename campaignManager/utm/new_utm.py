import streamlit as st
import uuid

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

def new_utm(activitydf,user_id,name):
    approveitems=st.columns([1, 1])
    with approveitems[0]:
        selCampaign=st.selectbox('choose approved activities',activitydf['activity_name'].unique(),key='selectcampaign')  
    with approveitems[1]:
        selAct=st.selectbox('choose approved activities',activitydf['activity_name'].unique(),key='selectactivities')  

    activity_grouping="KOL"
    activity_name='lala'
    activity_details="lulu"
    selected_campaign_id="asd"
    selected_campaign='asd'
    startDateActivity='2024-09-20'


    colau = st.columns([3, 3, 2, 3, 3, 2, 1, 1])
    with colau[0]:
        alias = st.text_input(f'Alias', key=f'alias')
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
        placement = st.selectbox(f'penempatan', tuple(list(sorted(placement)) + ['others']), key=f'placement_type')
        if placement == 'others':
            with colau[2]:
                placement = st.text_input(f'Other placement', 'new placement', key=f'placement')
                n = 1
        else:
            n = 0
    with colau[2 + n]:
        destination = st.selectbox(f'destination', ('web', 'app'), key=f'destination')
    with colau[3 + n]:
        if destination == 'web':
            destination_url = st.text_input(f'Enter URL', key=f'destination_url')
            
        if destination == 'app':
            destination_app = st.selectbox(f'Pilih destination app', ('home', 'product-detail', 'catalog', 'category', 'custom'), key=f'destination_app')
            with colau[4 + n]:
                if destination_app == 'custom':
                    final_deeplink_value = st.text_input(f'Deeplink path', key=f'final_deeplink')
               
                else:
                    business_unit = st.selectbox(f'Business unit', ('instant', 'super'), key=f'bu')
                    if destination_app != 'home':
                        with colau[5 + n]:
                            deeplink_id = st.text_input(f'Id value', key=f'deeplink')
                            final_deeplink_value = f'astro//{destination_app}/{deeplink_id}'
                         
                            if business_unit == 'super':
                                final_deeplink_value = f'{final_deeplink_value}?deliveryType=super'
                    else:
                        final_deeplink_value = 'astro//home'
    
    #if digital here
    
    buttonscol=st.columns([1,1,3])
    with buttonscol[0]:
        if st.button('generate', key=f'generate_utm'):
            #check alias, if error then do nothing
            #else generate and go back to home
            st.session_state['main_page'] = 'UTM'
            st.session_state['dynamic_menu'] = ['UTM','Campaigns','Activities','Promos','KV','Reports']
            st.rerun()

    with buttonscol[1]:
        if st.button('cancel', key=f'cancel'):
            st.session_state['main_page'] = 'UTM'
            st.session_state['dynamic_menu'] = ['UTM','Campaigns','Activities','Promos','KV','Reports']
            st.rerun()
                
  
    
    # # digital ads segment
    # if activity_grouping=='Digital Ads':
    
    #     cname=selected_campaign.split("_")[1]
    #     cid=selected_campaign.split("_")[0]
     
    #     campaign_level_naming=cid+"_"+name+"_"+str(startDateActivity).replace("-","")+"_"+cname
    #     ad_group_naming="audience/keywordGroupingTarget"
    #     ad_naming="kvName"+"_"+'kvId'
    #     if len(utmdf)>0:
    #         st.markdown("---")
    #         st.markdown(f"**Digital Ads Naming**") 

    #         adcampaign_list = []
    #         adgroupname_list = []
    #         adname_list = []
    
    #         for i in range(len(utmdf)):
                
    #             dacols = st.columns([1, 1, 1])
    #             with dacols[0]:
    #                 campaign_level_naming = cid + "_" + name + "_" + str(startDateActivity).replace("-", "") + "_" + cname
    #                 adcampaign = st.text_input(f'Suggested campaign name {i + 1}', campaign_level_naming, key=f'adcampaign_{i}')
    #                 adcampaign_list.append(adcampaign)  # Append each ad campaign name
    #             with dacols[1]:
    #                 ad_group_naming = "audience/keywordGroupingTarget"
    #                 adgroupname = st.text_input(f'Ad group/set name {i + 1}', ad_group_naming, key=f'adgroupname_{i}')
    #                 adgroupname_list.append(adgroupname)  # Append each ad group name
    #             with dacols[2]:
    #                 ad_naming = "ganti ini"+"|"+utmdf['utmid'][i]
    #                 adname = st.text_input(f'Ad name {i + 1}', ad_naming, key=f'adname_{i}')
    #                 adname_list.append(adname)  # Append each ad name
          
    #         # Now replicate the adcampaign, adgroupname, and adname columns in the dataframe
    #         utmdf['adcampaign'] = adcampaign_list
    #         utmdf['adgroupname'] = adgroupname_list
    #         utmdf['adname'] = adname_list
  
    #     else:
    #         st.write('Make utm to create ad names')
    # else:
    #     utmdf['adcampaign'] = None
    #     utmdf['adgroupname'] = None
    #     utmdf['adname'] = None