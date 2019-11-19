

from flask import Flask, request, render_template
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.targetingsearch import TargetingSearch
from facebook_business.adobjects.targeting import Targeting
import datetime
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adimage import AdImage
app = Flask(__name__)
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Gideon12",
    database = "FacebookAds"
)

campaign_name = ""
location = ""
demographics_age_min = ""
demographics_age_max = ""
adset_name = ""
image_path = ""
creative_name = ""
ad_name =  ""
gender = ""

#initialize connection to MYSQL table so as to populate user data
mycursor = mydb.cursor()
 
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':

        campaign_name = request.form['campaign_name']
        location = request.form['location']
        demographics_age_min = request.form['age_max']
        demographics_age_max = request.form['age_min']
        adset_name = request.form['adset_name']
        image_path = request.form['image_path']
        creative_name = request.form['creative_name']
        ad_name =  request.form['ad_name']
        gender = request.form['gender']
        mycursor.execute("INSERT INTO adsData (campaign_name, location, age_min, age_max, ad_name, Gender) VALUES (%s, %s, %s, %s, %s, %s)", (campaign_name, location, demographics_age_min, demographics_age_max, ad_name, gender))
    
        mydb.commit()

        return render_template('index.html')

    else:
        return render_template('index.html')

@app.route('/createAd')
def create_ad():
    campaign_name = request.args.get('campaign_name')
    location = request.args.get('location')
    demographics_age_min = request.args.get('age_max')
    demographics_age_max = request.args.get('age_min')
    adset_name = request.args.get('adset_name')
    image_path = request.args.get('image_path')
    creative_name = request.args.get('creative_name')
    ad_name =  request.args.get('ad_name')
    gender = request.args.get('gender')  
 
    access_token = 'EAAIA2D5EZA7kBAEpSkuodKf6smQzTdESBDqHPiDmPFciHVpxlTI7iLNTGZCOajWKVTVKo5nZAwsDGuGZC5y376b789T7QLxxhhreRHCuhHYV3OU7Yt8sHweq7f4IVSWSHXLoSecKZAQC7Rs2vglXBJ4yKD9iNwZBR2BpPjfQV2jsY8IzuUpTXa5me81jhZCpYWhmJyLhBYL1gZDZD'
    app_secret = '6ce7390fe1cd13d86c41474627d6b650'
    app_id = '563878711027641'
    ad_account_id = 'act_215421109'
    page_id = ''
    FacebookAdsApi.init(access_token=access_token)
    
    params = {

        'name': campaign_name,
        'objective': 'POST_ENGAGEMENT',
        'status': 'ACTIVE',
        'special_ad_category': 'CREDIT',
    }

    campaign_result = AdAccount(ad_account_id).create_campaign(params=params)
    print(campaign_result)

    today = datetime.date.today()
    start_time = str(today)
    end_time = str(today + datetime.timedelta(weeks=1))

    adset = AdSet(parent_id=ad_account_id)
    adset.update({
        'name': adset_name,
        'campaign_id': campaign_result["id"],
        'daily_budget': 150,
        'billing_event': 'IMPRESSIONS',
        'optimization_goal': 'REACH',
        'bid_amount': 10,
        'targeting': {'geo_locations': {'countries': {location}},
                    'publisher_platforms': 'facebook'},
        'start_time': start_time,
        'end_time': end_time,
    })
    fields = [
    ]

    params={'status': 'ACTIVE',}

    AdAccount(ad_account_id).create_ad_set(
    params=params,
    )

    #adset.create_ad_Set(params={'status': 'ACTIVE'})

    image = AdImage(parent_id=ad_account_id)
    image[AdImage.Field.filename] = image_path
    image.remote_create()

    image_hash = image[AdImage.Field.hash]
    print(image)

    fields = [
    ]
    params = {
    'name': creative_name,
    'object_story_spec': {'page_id':page_id,'link_data':{'image_hash':image_hash,'link':'www.facebook.com','message':'none'}},
    }
    adcreative = AdAccount(ad_account_id).create_ad_creative(fields=fields, params=params)
    print(adcreative)

    fields = [
    ]
    params = {
    'name': ad_name,
    'adset_id': adset['id'],
    'creative': {'creative_id': adcreative['creative_id']},
    'status': 'ACTIVE'
    }
    print(AdAccount(ad_account_id).create_ad(fields=fields, params=params))


            
if __name__ == '__main__':
    app.run()



 



