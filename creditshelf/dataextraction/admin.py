from django.contrib import admin
from .models import Place, Crash, Harmed, Vehicle, Station, Bike, Trip


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('collision_id', 'borough', 'location_lat', 'location_log')


@admin.register(Crash)
class CrashAdmin(admin.ModelAdmin):
    list_display = ('collision_id', 'date_of_crash', 'time_of_crash')


@admin.register(Harmed)
class HarmedAdmin(admin.ModelAdmin):
    list_display = ('collision_id', 'no_injured', 'no_killed')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('collision_id', 'veh_type_1', 'veh_type_2', 'veh_type_3', 'veh_type_4', 'veh_type_5')


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('station_name', 'location_lat', 'location_log', 'station_id')


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = (
    'start_time', 'stop_time', 'start_station_id', 'stop_station_id', 'bike_id', 'usertype', 'yod', 'gender')
