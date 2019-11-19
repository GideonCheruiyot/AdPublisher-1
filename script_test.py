
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.targetingsearch import TargetingSearch
from facebook_business.adobjects.targeting import Targeting
import datetime
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adimage import AdImage

access_token = 'EAAIA2D5EZA7kBAFq68aSRmTM7nYZBv4IGBOSAhulWZBkZBPvMRfdRAsqVw30JAIoCMWEbKUYLYRAFYZB37UTMSOg1RZBQPdvXuqsPVqVNfRdF4kLyeA9hJ6nLZBN12wOYQG7LshCfzAZBdZAj7ICIwW0DBtZA2fd5iQSF4alEcZBoZBU3QZDZD'
app_secret = '6ce7390fe1cd13d86c41474627d6b650'
app_id = '563878711027641'
ad_account_id = 'act_215421109'
page_id = ''
FacebookAdsApi.init(access_token=access_token)
 

params = {

    'name': 'campaign',
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
    'name': 'adset',
    'campaign_id': campaign_result["id"],
    'daily_budget': 150,
    'billing_event': 'IMPRESSIONS',
    'optimization_goal': 'REACH',
    'bid_amount': 10,
    'targeting': {'geo_locations': {'countries': {'TR'}},
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
image[AdImage.Field.filename] = 'https://static.adweek.com/adweek.com-prod/wp-content/uploads/2019/01/pepsi-atlanta-super-bowl-hed-page-2019.jpg'
image.remote_create()

image_hash = image[AdImage.Field.hash]
print(image)

fields = [
]
params = {
  'name': 'creative',
  'object_story_spec': {'page_id':page_id,'link_data':{'image_hash':image_hash,'link':'www.facebook.com','message':'ad_message'}},
}
adcreative = AdAccount(ad_account_id).create_ad_creative(fields=fields, params=params)
print(adcreative)

fields = [
]
params = {
  'name': 'ad_name',
  'adset_id': adset['id'],
  'creative': {'creative_id': adcreative['creative_id']},
  'status': 'ACTIVE'
}
print(AdAccount(ad_account_id).create_ad(fields=fields, params=params))


