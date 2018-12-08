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
from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse

from views import (
    account_views,
    admin_views,
    top_views,
    search_views,
    nursery_views,
    misc_views
)
from views.profile_views import organizer_views, user_views
from views.api import locations, bookmarks


def ping(request):
    return HttpResponse('pong', 'application/json', status=200)


urlpatterns = [
    url(r'^api/v1/location/ward', locations.get_wards, name='get_wards'),
    url(r'^api/v1/location/station', locations.get_stations, name='get_stations'),
    url(r'^api/v1/location/near', locations.get_near_ward_and_stations,
        name='get_near_ward_and_stations'),
    url(r'^api/v1/bookmark/nursery/register', bookmarks.register_bookmark,
        name='register_nursery_bookmark'),

    url(r'^admin/wards/(?P<ward_id>\d+)/nurseries/(?P<nursery_id>\d+)/$', admin_views.nursery,
        name='admin_nursery_page'),
    url(r'^admin/wards/(?P<ward_id>\d+)/$', admin_views.nursery_list, name='admin_nurseries_page'),

    url(r'^nursery/(?P<nursery_id>\d+)/tour/(?P<nursery_tour_id>\d+)/(?P<reservation_id>\d+)/delete/$',
        nursery_views.delete_nursery_reservation, name='delete_user_reserved_page'),
    url(r'^nursery/(?P<nursery_id>\d+)/tour/(?P<nursery_tour_id>\d+)/reservation/(?P<reservation_id>\d+)/edit/$',
        nursery_views.nursery_reservation, name='edit_user_reserved_page'),
    url(r'^nursery/(?P<nursery_id>\d+)/tour/(?P<nursery_tour_id>\d+)/$', nursery_views.nursery_reservation,
        name='nursery_reservation_page'),
    url(r'^nursery/(?P<nursery_id>\d+)/$', nursery_views.nursery_detail, name='detail_page'),

    url(r'^contact/$', misc_views.contact, name='contact_page'),
    url(r'^about/$', misc_views.about, name='about_page'),
    url(r'^search/$', search_views.search_nurseries, name='search_page'),
    url(r'^ping', ping, name='ping'),

    url(r'^user/(?P<user_id>\d+)/nurseries/(?P<nursery_id>\d+)/tour/$',
        organizer_views.nursery_tour_profile,
        name='user_nursery_tour_page'),
    url(r'^user/(?P<user_id>\d+)/nurseries/(?P<nursery_id>\d+)/free/$',
        organizer_views.nursery_free_num_profile,
        name='user_nursery_free_num_page'),
    url(r'^user/(?P<user_id>\d+)/nurseries/(?P<nursery_id>\d+)/basic/$',
        organizer_views.nursery_basic_profile,
        name='user_nursery_basic_page'),
    url(r'^user/(?P<user_id>\d+)/nurseries/$', organizer_views.nursery_list_profile,
        name='user_nursery_list_page'),
    url(r'^user/(?P<user_id>\d+)/reserved/$', user_views.reserved_nurseries, name='user_reserved_page'),
    url(r'^user/(?P<user_id>\d+)/bookmarked/$', user_views.bookmarked_nurseries, name='user_bookmarked_page'),
    url(r'^user/(?P<user_id>\d+)/$', user_views.user_profile, name='user_profile_page'),

    url(r'^accounts/login/$', account_views.login_view, name='login_page'),
    url(r'^accounts/logout/$', account_views.logout_view, name='logout_page'),
    url(r'^accounts/signup/$', account_views.signup, name='signup_page'),
    url(r'^$', top_views.index, name='top_page')
]

if settings.ENV != 'PRODUCTION':
    urlpatterns += staticfiles_urlpatterns()
