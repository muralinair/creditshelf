from rest_framework import serializers
from dataextraction.models import Crash, Place, Harmed, Vehicle, Station


class DataextractionCrashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crash
        fields = '__all__'


class DataextractionPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class DataextractionHarmedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harmed
        fields = '__all__'


class DataextractionVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class DataextractionStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'
