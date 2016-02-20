from django.conf.urls import url
from advertisers.views.campaign_list import CampaignList
from advertisers.views.one_campaign import OneCampaignView

urlpatterns = [
    url(r'^campaigns/(?P<pk>\d+)/$', OneCampaignView.as_view()),
    url('^campaigns/', CampaignList.as_view())
]
