from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Device, Reading, Notification
from .serializers import ReadingSerializer, DeviceSerializer, NotificationSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from .helpers import air_comment, temperature_comment, humidity_comment
import datetime

# Create your views here.


@csrf_exempt
def current_reading(request):
    now = timezone.now()
    readings = Reading.objects.all().order_by('-timestamp')
    serializer = ReadingSerializer(readings, many=True)
    if len(serializer.data) == 0:
        data = {
            'air': {
                'name': 'Air',
                'value': 0,
                'comment': 'Comment',
            },
            'temperature': {
                'name': 'Temperature',
                'value': 0,
                'comment': 'Comment',
            },
            'humidity': {
                'name': 'Humidity',
                'value': 0,
                'comment': 'Comment',
            },
            'reading': {
                'reading_id': 0,
                'device_id': 0,
                'timestamp': now,
            }
        }
        return JsonResponse(data)
    data = {
        'air': {
            'name': 'Air',
            'value': serializer.data[0]['air'],
            'comment': air_comment(serializer.data[0]['air']),
        },
        'temperature': {
            'name': 'Temperature',
            'value': serializer.data[0]['temperature'],
            'comment': temperature_comment(serializer.data[0]['temperature']),
        },
        'humidity': {
            'name': 'Humidity',
            'value': serializer.data[0]['humidity'],
            'comment': humidity_comment(serializer.data[0]['humidity']),
        },
        'reading': {
            'reading_id': serializer.data[0]['reading_id'],
            'device_id': serializer.data[0]['device_id'],
            'timestamp': serializer.data[0]['timestamp'],
        }
    }
    return JsonResponse(data)


@csrf_exempt
def readings(request):
    """
    List all code reading, or create a new reading.
    """
    if request.method == 'GET':
        readings = Reading.objects.all()
        serializer = ReadingSerializer(readings, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ReadingSerializer(data=data)
        device = Device.objects.get(device_id=data['device_id'])
        notifications = Notification.objects.all().order_by(
            '-notification_timestamp')[0]
        if serializer.is_valid():
            serializer.save()

            # check if values are out of range and create notification
            if air_comment(
                    serializer.data['air']) == "Unhealthy" or air_comment(
                        serializer.data['air']
                    ) == "Very Unhealthy" or air_comment(
                        serializer.data['air']) == "Hazardous" or air_comment(
                            serializer.data['air']
                        ) == "Unhealthy for Sensitive Groups":
                # check if notification already exists
                if notifications.notification_type != "Air" and notifications.notification_message != "Air quality is " + air_comment(
                        serializer.data['air']):
                    notification = Notification.objects.create(
                        device_id=device,
                        notification_type="Air",
                        notification_message="Air quality is " +
                        air_comment(serializer.data['air']))
                    notification.save()
            if temperature_comment(
                    serializer.data['temperature']
            ) == "Very Hot" or temperature_comment(
                    serializer.data['temperature']) == "Hot":
                # check if notification already exists
                if notifications.notification_type != "Temperature" and notifications.notification_message != "Temperature is " + temperature_comment(
                        serializer.data['temperature']):
                    notification = Notification.objects.create(
                        device_id=device,
                        notification_type="Temperature",
                        notification_message="Temperature is " +
                        temperature_comment(serializer.data['temperature']))
                    notification.save()
            if humidity_comment(serializer.data['humidity']
                                ) == "Very Humid" or humidity_comment(
                                    serializer.data['humidity']) == "Humid":
                # check if notification already exists
                if notifications.notification_type != "Humidity" and notifications.notification_message != "Humidity is " + humidity_comment(
                        serializer.data['humidity']):
                    notification = Notification.objects.create(
                        device_id=device,
                        notification_type="Humidity",
                        notification_message="Humidity is " +
                        humidity_comment(serializer.data['humidity']))
                    notification.save()
            # delete notifications older than 24 hours
            Notification.objects.filter(
                notification_timestamp__lte=timezone.now() -
                datetime.timedelta(days=1)).delete()
            return JsonResponse(serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def reading_details(request, pk):
    """
    Retrieve, update or delete a code reading.
    """
    try:
        reading = Reading.objects.get(pk=pk)
    except Reading.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReadingSerializer(reading)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ReadingSerializer(reading, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        reading.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def devices(request):
    """
    List all code devices, or create a new device.
    """
    if request.method == 'GET':
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def device_details(request, pk):
    """
    Retrieve, update or delete a code device.
    """
    try:
        device = Device.objects.get(pk=pk)
    except Device.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DeviceSerializer(device)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DeviceSerializer(device, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        device.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# Get daily average of air quality, temperature and humidity for the last 7 days and return them as arrays of days and values


@csrf_exempt
def trends(request):
    now = timezone.now()
    readings = Reading.objects.filter(
        timestamp__gte=now - timezone.timedelta(days=7)).order_by(
            '-timestamp')  # get last 7 days of readings
    serializer = ReadingSerializer(readings, many=True)
    if len(serializer.data) == 0:
        data = {
            'air': {
                'name': 'Air',
                'days': [],
                'values': [],
            },
            'temperature': {
                'name': 'Temperature',
                'days': [],
                'values': [],
            },
            'humidity': {
                'name': 'Humidity',
                'days': [],
                'values': [],
            },
        }
        return JsonResponse(data)
    days = []
    air_values = []
    temperature_values = []
    humidity_values = []

    # get each day's average
    for data in serializer.data:
        #day = data['timestamp'].split('T')[0]
        date = datetime.datetime.strptime(data['timestamp'].split('T')[0],
                                          "%Y-%m-%d")
        day = date.strftime("%a")
        if day not in days:
            days.append(day)
            air_values.append(data['air'])
            temperature_values.append(data['temperature'])
            humidity_values.append(data['humidity'])
        else:
            index = days.index(day)
            air_values[index] = (air_values[index] + data['air']) / 2
            temperature_values[index] = (temperature_values[index] +
                                         data['temperature']) / 2
            humidity_values[index] = (humidity_values[index] +
                                      data['humidity']) / 2
    data = {
        'air': {
            'name': 'Air',
            'days': days,
            'values': air_values,
        },
        'temperature': {
            'name': 'Temperature',
            'days': days,
            'values': temperature_values,
        },
        'humidity': {
            'name': 'Humidity',
            'days': days,
            'values': humidity_values,
        },
    }
    return JsonResponse(data)


@csrf_exempt
def notifications(request):
    """
    List all code notifications, or create a new notification.
    """
    if request.method == 'GET':
        now = timezone.now()
        today = now.date()
        notifications = Notification.objects.filter(
            notification_timestamp__gte=today).order_by(
                '-notification_timestamp')[0:10]
        serializer = NotificationSerializer(notifications, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
