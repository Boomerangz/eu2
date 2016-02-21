"""eu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from eu import settings
from eu.views import home
from publishers.views.site_list import SiteList
from django.conf.urls.static import static



urlpatterns = patterns(
    url('^asdasd/', RedirectView.as_view(url='/')),
    url('^accounts/profile/', RedirectView.as_view(url='/')),
    url('^login/',
        auth_views.login,
        {'template_name': 'registration/login.html'}),
    url(r'^publisher/', include('publishers.urls', namespace="publisher")),
    url(r'^advertiser/', include('advertisers.urls', namespace="advertiser")),
    url('^admin/', admin.site.urls),
    url('', home),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




