from .serializer import \
    DataextractionCrashSerializer, \
    DataextractionPlaceSerializer, \
    DataextractionHarmedSerializer, \
    DataextractionVehicleSerializer, \
    DataextractionStationSerializer
from rest_framework.viewsets import ModelViewSet
from dataextraction.models import Crash, Place, Harmed, Vehicle, Station
from rest_framework import generics
from django.views.generic import TemplateView
from django.shortcuts import render
from creditshelf.settings import API_KEY


class Homepage(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {
            "server": request.META['HTTP_HOST'],
            "key": API_KEY,
        }
        return render(request, "index.html", context=context)


class CrashViewSet(ModelViewSet):
    serializer_class = DataextractionCrashSerializer
    queryset = Crash.objects.all()


class PlaceViewSet(generics.ListAPIView):
    serializer_class = DataextractionPlaceSerializer

    def get_queryset(self):
        borough = self.request.query_params.get("borough")
        queryset = Place.objects.all()
        if borough is not None:
            queryset = queryset.filter(borough=borough)
        return queryset


class HarmedViewSet(ModelViewSet):
    serializer_class = DataextractionHarmedSerializer
    queryset = Harmed.objects.all()


class VehicleViewSet(ModelViewSet):
    serializer_class = DataextractionVehicleSerializer
    queryset = Vehicle.objects.all()


class StationViewSet(ModelViewSet):
    serializer_class = DataextractionStationSerializer
    queryset = Station.objects.all()
