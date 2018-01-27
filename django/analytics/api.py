from rest_framework import routers, serializers, viewsets
from .models import *
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.db.models import Q

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
    queryset = Client.objects.all()
    def get(self,request,format=None):
        values = []
        client = Client.objects.get(ClientName=request.GET['user'])
        kiosk = Kiosk.objects.filter(Client=client)
        location = Location.objects.get(LocationName='Baltimore')
        print(Q(kiosk.filter(Location = location)))
        ids = request.GET.getlist('ID')
        if ids != []:
            for i in ids:
                temp = kiosk.get(ID=i)

        if request.GET.getlist('Past') == 'Day':
            print(0)
        return Response(values)


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
