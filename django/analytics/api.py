from rest_framework import routers, serializers, viewsets
from .models import *
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.db.models import Q
from .filters import *
import datetime
# Serializers define the API representation.
class TimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Time
        fields = ('TimeIn','TimeOut','pk')

# ViewSets define the view behavior.
class TimeViewSet(viewsets.ModelViewSet):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer


class PortSerializer(serializers.HyperlinkedModelSerializer):
    PortToTime = TimeSerializer(many=True,read_only=True)

    class Meta:
        model = Port
        fields = ('Port','Type','PortToTime')

# ViewSets define the view behavior.
class PortViewSet(viewsets.ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer

# Serializers define the API representation.
class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('LocationName',)

# ViewSets define the view behavior.
class LocaitonViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

# Serializers define the API representation.
class KioskSerializer(serializers.HyperlinkedModelSerializer):
    KioskToPort = PortSerializer(many=True,read_only=True)
    class Meta:
        model = Kiosk
        fields = ('ID','KioskToPort')

# ViewSets define the view behavior.
class KioskViewSet(viewsets.ModelViewSet):
    queryset = Kiosk.objects.all()
    serializer_class = KioskSerializer

# Serializers define the API representation.
class ClientSerializer(serializers.HyperlinkedModelSerializer):
    KioskToClient = KioskSerializer(many=True,read_only=True)
    class Meta:
        model = Client
        fields = ('ClientName','KioskToClient')
        depth = 1

# ViewSets define the view behavior.
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
# Serializers define the API representation.


class Search(APIView):
    renderer_classes = (JSONRenderer, )
    queryset = Kiosk.objects.all()
    def get(self,request,format=None):
        arr = []
        print('User:',request.user)
        if request.user.groups.filter(name='Admin').exists():
            qs = Kiosk.objects.all()
        elif request.user.groups.filter(name='Partner').exists():
            clients = PartnerToClient.objects.filter(Partner__PartnerName=request.user.username)
            qs = Kiosk.objects.filter(Client__in = clients.values('Client'))
        elif request.user.groups.filter(name='Client').exists():
            qs = Kiosk.objects.filter(Client__ClientName = request.user.username)
        else:
            qs = Kiosk.objects.none()
        print(qs)
        kioskFilter = KioskFilter(request.GET,qs)
        for kiosk in kioskFilter.qs:
            k = {}
            k['ID'] = kiosk.ID
            k['Client'] = kiosk.Client.ClientName
            k['Loc'] = kiosk.Location.LocationName
            ports = Port.objects.filter(Kiosk = kiosk)
            times = Time.objects.filter(Port__in = ports)
            print(times)
            k['Tot'] = times.count()
            last = times.latest('TimeOut').TimeOut.replace(tzinfo=None)
            k['last_update'] = last.strftime("%Y-%m-%d %H:%M:%S")
            if (datetime.datetime.now().replace(tzinfo=None)-last.replace(tzinfo=None)).days > 50:
                k['online'] = False
            else:
                k['online'] = True
            arr.append(k)
        return Response(arr)


# class SkillCount(APIView):
#     renderer_classes = (JSONRenderer, )
#     queryset = PersonToSkills.objects.all()
#     def get(self, request, format=None):
#         print(request.GET)
#         arr =[]
#         for skill in Skills.objects.all():
#             d = {}
#             d['name'] = skill.Name
#             d['count']= PersonToSkills.objects.filter(SkillsID=skill.pk).count()
#             arr.append(d)
#         new_arr = list(reversed(sorted(arr,key=lambda k:k['count'])))
#         print(new_arr[0:10])
#         return Response(new_arr[0:10])
