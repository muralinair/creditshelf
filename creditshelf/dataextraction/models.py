from django.db import models
from django.core.validators import MaxValueValidator


class Crash(models.Model):
    collision_id = models.IntegerField(unique=True, primary_key=True)
    date_of_crash = models.DateField()
    time_of_crash = models.TimeField()

    def __str__(self):
        return str(self.collision_id)


class Place(models.Model):
    borough = models.CharField(max_length=64)
    zip = models.IntegerField()
    location_lat = models.DecimalField(max_digits=10, decimal_places=8)
    location_log = models.DecimalField(max_digits=10, decimal_places=8)
    on_street = models.CharField(max_length=64)
    off_street = models.CharField(max_length=64)
    cross_street = models.CharField(max_length=64)
    collision_id = models.ForeignKey(Crash, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.borough}/{str(self.zip)}"


class Harmed(models.Model):
    ped_injured = models.IntegerField()
    ped_killed = models.IntegerField()
    cycl_injured = models.IntegerField()
    cycl_killed = models.IntegerField()
    motor_injured = models.IntegerField()
    motor_killed = models.IntegerField()
    collision_id = models.ForeignKey(Crash, on_delete=models.CASCADE)

    @property
    def no_injured(self):
        return self.ped_injured + self.cycl_injured + self.motor_injured

    @property
    def no_killed(self):
        return self.ped_killed + self.cycl_killed + self.motor_killed

    def __str__(self):
        return f"{str(self.no_injured)}/{str(self.no_killed)}"


class Vehicle(models.Model):
    veh_type_1 = models.CharField(max_length=64)
    veh_type_2 = models.CharField(max_length=64)
    veh_type_3 = models.CharField(max_length=64)
    veh_type_4 = models.CharField(max_length=64)
    veh_type_5 = models.CharField(max_length=64)
    collision_id = models.ForeignKey(Crash, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.veh_type_1}/{self.veh_type_2}"


class Station(models.Model):
    station_name = models.CharField(max_length=64)
    location_lat = models.DecimalField(max_digits=10, decimal_places=8)
    location_log = models.DecimalField(max_digits=10, decimal_places=8)
    station_id = models.IntegerField(unique=True, primary_key=True)

    def __str__(self):
        return f"{self.station_id}"


class Bike(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)

    def __str__(self):
        return f"{self.id}"


class Trip(models.Model):
    USER_CHOICES = [
        ("Subscriber", "Subscriber"),
        ("Customer", "Customer"),
        ("None", "None"),
    ]
    USER_GENDER = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3)
    ]
    usertype = models.CharField(choices=USER_CHOICES, max_length=64)
    yod = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    gender = models.IntegerField(choices=USER_GENDER)
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    start_station_id = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="start_station_id")
    stop_station_id = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="stop_station_id")
    bike_id = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name="bike_id")

    @property
    def duration(self):
        return self.stop_time - self.start_time
