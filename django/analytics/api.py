from rest_framework import routers, serializers, viewsets
from .models import *
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.db.models import Q
from .filters import *
import datetime
from .views import filter_dates
from django.db.models import Sum
import pytz

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

def TypeOfChargePie(ports,times):
    a = ports.filter(Type='Android')
    i = ports.filter(Type='IPhone')
    u = ports.filter(Type='USB-C')
    o = ports.filter(Type='Other')
    android = times.filter(Port__in =a)
    iphone =  times.filter(Port__in =i)
    usbc =  times.filter(Port__in =u)
    other =  times.filter(Port__in =o)
    total = iphone.count()+android.count()+usbc.count()+other.count()
    try:
        a_percent = str(int(100*(android.count()/total)))
    except ZeroDivisionError:
        a_percent=str(0)
    try:
        i_percent = str(int(100*(iphone.count()/total)))
    except ZeroDivisionError:
        i_percent=str(0)
    try:
        u_percent = str(int(100*(usbc.count()/total)))
    except ZeroDivisionError:
        u_percent=str(0)
    try:
        o_percent = str(int(100*(other.count()/total)))
    except ZeroDivisionError:
        o_percent=str(0)

    val = [{'x':'Android-'+a_percent+'%','y':android.count()},{'x':'IPhone-'+i_percent+'%','y':iphone.count()},\
    {'x':'USB-C-'+u_percent+'%','y':usbc.count()},{'x':'Other-'+o_percent+'%','y':other.count()}]
    data={
        'label':'TypeOfChare',
        'values':val
        }

    return data
def TimeOfDayBar(times):
    val = []
    for i in range(9,19):
        val.append({'x':datetime.datetime.now().replace(hour=i).time().strftime("%I%p"),'y':times.filter(TimeOut__hour=i).count()})
    data = [{
    'label':'TimeOfDay',
    'values':val
    }]
    return data
class Dashboard(APIView):
    renderer_classes = (JSONRenderer, )
    queryset = Kiosk.objects.all()
    def get(self,request,format=None):
        val = {}
        if request.user.groups.filter(name='Admin').exists():
            qs = Kiosk.objects.all()
        elif request.user.groups.filter(name='Partner').exists():
            clients = PartnerToClient.objects.filter(Partner__User=request.user)
            qs = Kiosk.objects.filter(Client__in = clients.values('Client'))
        elif request.user.groups.filter(name='Client').exists():
            qs = Kiosk.objects.filter(Client__User = request.user)
        else:
            qs = Kiosk.objects.none()
        kioskFilter = KioskFilter(request.GET,qs)
        ports = Port.objects.filter(Kiosk__in =kioskFilter.qs)
        times = Time.objects.filter(Port__in = ports)
        times = filter_dates(times,request.GET)
        val['count'] = times.count()
        try:
            val['avg'] = int(times.aggregate(Sum('Duration'))['Duration__sum']/times.count())
        except TypeError:
            val['avg'] = 0
        val['TypeOfCharge'] = TypeOfChargePie(ports,times)
        val['TimeOfDay'] = TimeOfDayBar(times)
        return Response(val)

class KioskDetails(APIView):
    renderer_classes = (JSONRenderer, )
    queryset = Kiosk.objects.all()
    def get(self,request,format=None):

        print('request',request.GET)
        partner = False
        client = False
        admin = False
        kID = request.GET.get('ID',None)
        kiosk = Kiosk.objects.get(ID=kID)
        if request.user.groups.filter(name='Partner').exists():
            partner = PartnerToKiosk.objects.get(Partner__User = request.user, Kiosk= kiosk)
        elif request.user.groups.filter(name='Client').exists():
            client  = request.user == kiosk.Client.User
        elif request.user.groups.filter(name='Admin').exists():
            admin = True
        else:
            print('not authorized')
        if admin or partner or client:
            online = False
            port_arr = []
            port = Port.objects.filter(Kiosk=kiosk)
            times = Time.objects.filter(Port__in=port)
            times = filter_dates(times,request.GET)
            for p in port:
                print("Port:",p,' pk ',p.pk)
                try:
                    temp_time = times.filter(Port= p)
                    last_update = temp_time.latest('TimeOut').TimeOut
                    total_count = temp_time.count()
                    elasped_time =  last_update - datetime.datetime.now()
                    if elasped_time.days < -20:
                        flag = True
                    else:
                        flag = False
                        online = True
                except Time.DoesNotExist:
                    last_update = None
                    total_count = 0
                    flag = True
                port_arr.append({'pk':p.pk,'Type':p.Type,'Port':p.Port,'Last_Update':last_update.strftime("%m/%d/%Y %I:%M:%S %p"),'Flag':flag,'Total':total_count})
        return Response({'ports':port_arr,'online':online})

class Search(APIView):
    renderer_classes = (JSONRenderer, )
    queryset = Kiosk.objects.all()
    def get(self,request,format=None):
        arr = []
        print('User:',request.user)
        if request.user.groups.filter(name='Admin').exists():
            qs = Kiosk.objects.all()
        elif request.user.groups.filter(name='Partner').exists():
            clients = PartnerToKiosk.objects.filter(Partner__User=request.user)
            qs = Kiosk.objects.filter(ID__in = clients.values('Kiosk_id'))
        elif request.user.groups.filter(name='Client').exists():
            qs = Kiosk.objects.filter(Client__User = request.user)
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
            k['Tot'] = times.count()
            try:
                last = times.latest('TimeOut').TimeOut
                k['last_update'] = last.strftime("%m/%d/%Y %I:%M:%S %p")
                if (datetime.datetime.now().replace(tzinfo=None)-last.replace(tzinfo=None)).days > 50:
                    k['online'] = False
                else:
                    k['online'] = True
            except Time.DoesNotExist:
                k['last_update'] = None
                k['online'] = False
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
