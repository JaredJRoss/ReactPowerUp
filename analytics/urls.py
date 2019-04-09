from django.conf.urls import url, include
from . import views
from .views import *
from rest_framework import routers, serializers, viewsets
from .api import *
from django.views import generic
from django.contrib.auth import views as auth_views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'client', ClientViewSet)
router.register(r'location',LocaitonViewSet)
router.register(r'kiosk',KioskViewSet)
router.register(r'port',PortViewSet)
router.register(r'time',TimeViewSet)
app_name = 'analytics'


urlpatterns=[
    url(r'^upload/$',upload, name='upload',),
    url(r'^$',mainpage,name='home'),
    url(r'add_location',make_location,name="addLocation"),
    url(r'add_kiosk/$',make_kiosk, name='add_kiosk'),
    url(r'edit_port/(?P<pk>\d+)$',edit_port,name='edit_port'),
    url(r'edit_kiosk/(?P<pk>\d+)$',edit_kiosk,name='edit_kiosk'),
    url(r'reset_kisok/(?P<pk>\d+)/$',resetKiosk,name="reset_kiosk"),
    url(r'editClient/$',edit_client,name='editClient'),
    url(r'editLocation/$',edit_location,name='editLocation'),
    url(r'editPartner/$',edit_partner,name='editPartner'),
    url(r'delete-kiosk/(?P<pk>\d+)/$',deleteKiosk,name='delete-kiosk'),
    url(r'delete-partner/(?P<pk>\d+)/$',deletePartner,name='delete-partner'),
    url(r'delete-location/(?P<pk>\d+)/$',deleteLocation,name='delete-location'),
    url(r'delete-client/(?P<pk>\d+)/$',deleteClient,name='delete-client'),
    url(r'^client-autocomplete/$',ClientAutoComplete.as_view(create_field='ClientName'), name='client-autocomplete', ),
    url(r'^location-autocomplete/$',LocationAutoComplete.as_view(create_field='LocationName'), name='location-autocomplete', ),
    url(r'^kiosk-autocomplete/$',KioskAutoComplete.as_view(), name='kiosk-autocomplete', ),
    url(r'^type-autocomplete/$',TypeAutoComplete.as_view(create_field='Type'), name='type-autocomplete', ),
    url(r'^partner-autocomplete/$',PartnerAutoComplete.as_view(create_field='PartnerName'), name='partner-autocomplete', ),
    url(r'^api/', include(router.urls)),
    url(r'^api/search$', Search.as_view(), name='search'),
    url(r'^api/dash$', Dashboard.as_view(), name='dash'),
    url(r'^api/kiosk$',KioskDetails.as_view()),
    url(r'kiosk/(?P<pk>\d+)$', kiosk_view, name='kiosk'),
    url(r'^login/$', auth_views.login,{'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'analytics:login'},name='logout'),
    url(r'^signupPartner/$', signupPartner, name='signupPartner'),
    url(r'^signupClient/$', signupClient, name='signupClient'),
    url(r'^signupAdmin/$', signupAdmin, name='signupAdmin'),
    url(r'pdf/',PDF,name="test")

]
