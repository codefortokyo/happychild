"""happy_child URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.http import HttpResponse

from views import account_views, admin_views, top_views, search_views, detail_views, misc_views
from views.api import location


def ping(request):
    return HttpResponse('pong', 'application/json', status=200)


urlpatterns = [
    url(r'^api/v1/location/ward', location.get_wards, name='get_wards'),
    url(r'^api/v1/location/station', location.get_stations, name='get_stations'),
    url(r'^api/v1/location/near', location.get_near_ward_and_stations, name='get_near_ward_and_stations'),

    url(r'^admin/wards/(?P<ward_id>\d+)/nurseries/(?P<nursery_id>\d+)/', admin_views.nursery,
        name='admin_nursery_page'),
    url(r'^admin/wards/(?P<ward_id>\d+)', admin_views.nursery_list, name='admin_nurseries_page'),

    url(r'^nursery/(?P<nursery_id>\d+)', detail_views.nursery_detail, name='detail_page'),
    url(r'^contact', misc_views.contact, name='contact_page'),
    url(r'^about', misc_views.about, name='about_page'),
    url(r'^search', search_views.search_nurseries, name='search_page'),
    url(r'^ping', ping, name='ping'),

    url(r'^user/(?P<user_id>\d+)/', account_views.user_profile, name='user_profile_page'),
    url(r'^login', account_views.login_view, name='login_page'),
    url(r'^logout', account_views.logout_view, name='logout_page'),
    url(r'^signup', account_views.signup, name='signup_page'),
    url(r'^', top_views.index, name='top_page')
]
