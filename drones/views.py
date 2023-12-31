from rest_framework import authentication
from rest_framework import generics
from rest_framework import filters
from rest_framework import permissions
from rest_framework import throttling
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .filters import CompetitionFilter
from .models import (
    Competition,
    DroneCategory,
    Drone,
    Pilot
)
from .permissions import IsCurrentUserOwnerOrReadOnly
from .serializers import (
    DroneCategorySerializer,
    DroneSerializer,
    CompetitionSerializer,
    PilotSerializer,
    PilotCompetitionSerializer
)

class DroneCategoryList(generics.ListCreateAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-list'
    filterset_fields = ('name',)
    search_fields = ('name',)
    ordering_fields = ('name',)

class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-detail'

class DroneList(generics.ListCreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-list'
    throttle_classes = (throttling.ScopedRateThrottle,)
    throttle_scope = 'drones'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, 
        IsCurrentUserOwnerOrReadOnly
    )
    filterset_fields = (
        'name',
        'drone_category',
        'manufacturing_date',
        'has_it_competed'
    )
    search_fields = ('name',)
    ordering_fields = (
        'name',
        'manufacturing_date'
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, 
        IsCurrentUserOwnerOrReadOnly
    )
    throttle_classes = (throttling.ScopedRateThrottle,)
    throttle_scope = 'drones'

class PilotList(generics.ListCreateAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-list'
    throttle_classes = (throttling.ScopedRateThrottle,)
    throttle_scope = 'pilots'
    filterset_fields = (
        'name',
        'gender',
        'races_count'
    )
    search_fields = ('name',)
    ordering_fields = (
        'name',
        'races_count'
    )
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-detail'
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    throttle_classes = (throttling.ScopedRateThrottle,)
    throttle_scope = 'pilots'

class CompetitionList(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-list'
    filter_class = CompetitionFilter
    ordering_fields = (
        'distance_in_feet',
        'distance_achievement_date'
    )

class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-detail'

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    
    def get(self, request, *args, **kwargs):
        return Response({
            'drone-categories': reverse(DroneCategoryList.name, request=request),
            'drones': reverse(DroneList.name, request=request),
            'pilots': reverse(PilotList.name, request=request),
            'competitions': reverse(CompetitionList.name, request=request),
        })