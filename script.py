
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.targetingsearch import TargetingSearch
from facebook_business.adobjects.targeting import Targeting
import datetime
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adimage import AdImage

access_token = 'EAAIA2D5EZA7kBAJmUlFReIeuUZBVucx7dAaU3mTwjDuyvN9ZAvuvivm5UEeytPbFyup7Xm1b2kEVogvtIWUCMVC6Buq7K3CR4G1wV1wjBYTpViYJJhMmWlNFZBP3SScPTXo4ipBIF5d25CCBT9Fr1vslix7f1HqvNj74Fx3862RnKhbsJJydY41MzjzLZBXQdWGuuuqgRSNg5Q2ArJtpZA0WMtTGf2rlHRSZCZA92tuZB9gZDZD'
app_secret = '6ce7390fe1cd13d86c41474627d6b650'
app_id = '563878711027641'
ad_account_id = 'act_215421109'
page_id = '113893613377855'
FacebookAdsApi.init(access_token=access_token)
 

params = {

    'name': 'campaign_name',
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
    'name': 'giddy',
    'campaign_id': campaign_result["id"],
    'daily_budget': 150,
    'billing_event': 'IMPRESSIONS',
    'optimization_goal': 'REACH',
    'bid_amount': 10,
    'targeting': {'geo_locations': {'countries': 'US'},
                  'publisher_platforms': 'facebook'},
    'start_time': start_time,
    'end_time': end_time,
})
fields = [
]


adset.remote_create(params={
    'status': AdSet.Status.paused,
})

# adset.create(params={'status': 'ACTIVE'})

#adset.create_ad_Set(params={'status': 'ACTIVE'})

print(adset)




image = AdImage(parent_id=ad_account_id)
image[AdImage.Field.filename] = '/Users/mercytich/Desktop/download.jpeg'
image.remote_create()

image_hash = image[AdImage.Field.hash]
print(image)

fields = [
]
params = {
  'name': 'creative__name',
  'object_story_spec': {'page_id': page_id,'link_data':{'image_hash':image_hash,'link':'https://www.facebook.com/TechTutor-113893613377855/?modal=admin_todo_tour','message':'ad here'}},
}
adcreative = AdAccount(ad_account_id).create_ad_creative(fields=fields, params=params)

fields = [
]

params = {
  'name': 'ad__name',
  'adset_id': adset['id'],
  'creative': {'creative_id': adcreative['creative_id']},
  'status': 'ACTIVE'
}
ad = AdAccount(ad_account_id).create_ad(fields=fields, params=params)

print(adcreative)


