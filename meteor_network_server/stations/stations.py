from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from .hosts import Host

import uuid

class Station(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=128, default="Unnamed Station")
    latitude = models.FloatField(default=None, null=True)
    longitude = models.FloatField(default=None, null=True)
    height = models.FloatField(default=None, null=True)
    temperature = models.FloatField(default=None, null=True)
    humidity = models.FloatField(default=None, null=True)
    disk_used = models.FloatField(default=None, null=True)
    disk_cap = models.FloatField(default=None, null=True)
    last_updated = models.DateTimeField(default=timezone.now)
    host = models.ForeignKey(Host, default=None, null=True, on_delete=models.CASCADE)

class TelemetryLog(models.Model):
    temperature = models.FloatField(default=None, null=True)
    humidity = models.FloatField(default=None, null=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

class StationError(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    error = models.TextField(max_length=512)

def update_station_data(station, data):
    if 'name' in data: station.name = data['name']

    if 'latitude' in data:
        station.latitude = data['latitude']
    else:
        station.latitude = None
    if 'longitude' in data:
        station.longitude = data['longitude']
    else:
        station.longitude = None
    if 'height' in data:
        station.height = data['height']
    else:
        station.height = None

    telemetry_log = TelemetryLog()

    telemetry_log.station = station
    if 'temperature' in data:
        station.temperature = data['temperature']
        telemetry_log.temperature = data['temperature']
    else:
        station.temperature = None

    if 'humidity' in data:
        station.humidity = data['humidity']
        telemetry_log.humidity = data['humidity']
    else:
        station.humidity = None

    telemetry_log.timestamp = timezone.now()

    if 'disk_used' in data and 'disk_cap' in data:
        station.disk_used = data['disk_used']
        station.disk_cap = data['disk_cap']
    else:
        station.disk_used = None
        station.disk_cap = None

    if 'host' in data:
        host_data = data['host']

        try:
            if 'email' in host_data:
                host = Host.objects.get(email=host_data['email'])
            elif 'name' in host_data:
                host = Host.objects.get(name=host_data['name'])
        except Host.DoesNotExist:
            host = None

        if host == None:
            host = Host()

        if 'name' in host_data: host.name = host_data['name']
        if 'phone' in host_data:
            host.phone = host_data['phone']
        else:
            host.phone = None
        if 'email' in host_data:
            host.email = host_data['email']
        else:
            host.email = None
        if 'comment' in host_data:
            host.comment = host_data['comment']
        else:
            host.comment = None

        host.save()
        station.host = host

    station.last_updated = timezone.now()
    station.save()
    telemetry_log.save()

def register(data):
    try:
        if 'name' in data: station = Station.objects.get(name=data['name'])
    except Station.DoesNotExist:
        station = None

    if station == None:
        id = uuid.uuid4().hex
        station = Station()
        station.id = id

    update_station_data(station, data)

    return station.id

def get(id):
    return Station.objects.get(id=id)

def update(id, data):
    try:
        station = get(id)
    except Station.DoesNotExist:
        return False

    update_station_data(station, data)

    return True

def error(id, error):
    station = get(id)
    if station == None:
        return False

    station_error = StationError()
    station_error.station = station
    station_error.error = error
    station_error.save()

    return True

def get_current_list():
    return Station.objects.order_by('name')

def get_errors(id):
    return StationError.objects.filter(station=id)