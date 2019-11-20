

from flask import Flask, request, render_template,  redirect, url_for       
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
        image_path = '/Users/mercytich/Desktop/download.jpeg'
        image_link = 'https://www.facebook.com/TechTutor-113893613377855/?modal=admin_todo_tour'
        creative_name = request.form['creative_name']
        ad_name =  request.form['ad_name']
        gender = request.form['gender']

        print(campaign_name)
        print(location)

        mycursor.execute("INSERT INTO adsData (campaign_name, location, age_min, age_max, ad_name, Gender) VALUES (%s, %s, %s, %s, %s, %s)", (campaign_name, location, demographics_age_min, demographics_age_max, ad_name, gender))
        mydb.commit()
     
        access_token = 'REPLACE WITH ACCESS TOKEN'
        app_secret = 'REPLACE WITH APP SECRET'
        app_id = 'REPLACE WITH APP ID'
        ad_account_id = 'REPLACE WITH APP ID ACCOUNT'
        page_id = 113893613377855
        FacebookAdsApi.init(access_token=access_token)
         

        params = {

            'name': campaign_name,
            'objective': 'POST_ENGAGEMENT',
            'status': 'ACTIVE',
            'special_ad_category': 'NONE',
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
            'targeting': {'geo_locations': {'countries': location},
                        "age_min": demographics_age_min,
                        "age_max": demographics_age_max,
                        'publisher_platforms': 'facebook'
                          },
            'start_time': start_time,
            'end_time': end_time,
        })
        fields = [
        ]


        adset.remote_create(params={
            'status': AdSet.Status.paused,
        })


        print(adset)
        image = AdImage(parent_id=ad_account_id)
        image[AdImage.Field.filename] = image_path
        image.remote_create()

        image_hash = image[AdImage.Field.hash]
        print(image)

        fields = [
        ]
        params = {
          'name': creative_name,
          'object_story_spec': {'page_id': page_id,'link_data':{'image_hash':image_hash,'link':image_link}},
        }
        adcreative = AdAccount(ad_account_id).create_ad_creative(fields=fields, params=params)

        fields = [
        ]

        params = {
          'name': ad_name,
          'adset_id': adset['id'],
          'creative': {'creative_id': adcreative['creative_id']},
          'status': 'ACTIVE'
        }
        ad = AdAccount(ad_account_id).create_ad(fields=fields, params=params)

        return render_template('index.html')

    else:

        #return campaign_name, location, demographics_age_min, demographics_age_max, adset_name, image_path, creative_name, ad_name, gender

        return render_template('index.html')

            
if __name__ == '__main__':
    app.debug = True
    app.run()



 



