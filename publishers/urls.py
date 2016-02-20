from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from publishers.views.site_list import SiteList
from publishers.views.one_site import OneSiteView

urlpatterns = [
    url(r'^sites/(?P<pk>\d+)/$', OneSiteView.as_view()),
    url('^sites/', SiteList.as_view())

]
