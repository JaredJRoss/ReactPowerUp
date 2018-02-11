from django.conf.urls import url, include
from . import views
from .views import *
from rest_framework import routers, serializers, viewsets
from .api import *
from django.views import generic



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
    url(r'add_user/$',make_user, name='add_user',),
    url(r'^client-autocomplete/$',ClientAutoComplete.as_view(create_field='ClientName'), name='client-autocomplete', ),
    url(r'^location-autocomplete/$',LocationAutoComplete.as_view(create_field='LocationName'), name='location-autocomplete', ),
    url(r'^kiosk-autocomplete/$',KioskAutoComplete.as_view(), name='kiosk-autocomplete', ),
    url(r'^type-autocomplete/$',TypeAutoComplete.as_view(create_field='Type'), name='type-autocomplete', ),
    url(r'^api/', include(router.urls)),
    url(r'^api/search$', Search.as_view(), name='search'),
    url(r'kiosk/(?P<pk>\d+)$', kiosk_view, name='kiosk'),
    url(r'search/$',search,name='search')

]
