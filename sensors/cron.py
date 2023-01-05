from .models import Device, Reading, Notification
from .helpers import air_comment, temperature_comment, humidity_comment
from django.utils import timezone
import datetime


def send_notification():
    reading = Reading.objects.all().order_by('-timestamp')[0]
    device = Device.objects.get(device_id=1)
    notifications = Notification.objects.all().order_by(
        '-notification_timestamp')[0]

    # check for air quality is unhealthy, very unhealthy or harzadous and send notification
    if air_comment(reading.air) == 'Unhealthy' or air_comment(
            reading.air) == 'Very Unhealthy' or air_comment(
                reading.air) == 'Hazardous' or air_comment(
                    reading.air) == 'Unhealthy for Sensitive Groups':

        # check if notification is already sent
        if notifications.notification_type != 'Air Quality' and notifications.notification_message != f"Air quality is {air_comment(reading.air)}":
            notification = Notification.objects.create(
                notification_type='Air Quality',
                notification_message=
                f"Air quality is {air_comment(reading.air)}",
                device_id=device,
            )
            notification.save()

    # check for temperature is cold, very cold, hot and send notification
    if temperature_comment(
            reading.temperature) == 'Cold' or temperature_comment(
                reading.temperature) == 'Very Cold' or temperature_comment(
                    reading.temperature) == 'Hot':
        # check if notification is already sent
        if notifications.notification_type != 'Temperature' and notifications.notification_message != f"Temperature is {temperature_comment(reading.temperature)}":
            notification = Notification.objects.create(
                notification_type='Temperature',
                notification_message=
                f"Temperature is {temperature_comment(reading.temperature)}",
                device_id=device,
            )
            notification.save()

    # check for humidity is dry, very dry, humid and send notification
    if humidity_comment(reading.humidity) == 'Dry' or humidity_comment(
            reading.humidity) == 'Very Dry':
        # check if notification is already sent
        if notifications.notification_type != 'Humidity' and notifications.notification_message != f"Humidity is {humidity_comment(reading.humidity)}":
            notification = Notification.objects.create(
                notification_type='Humidity',
                notification_message=
                f"Humidity is {humidity_comment(reading.humidity)}",
                device_id=device,
            )
            notification.save()

    # delete notifications older than 24 hours
    Notification.objects.filter(notification_timestamp__lte=timezone.now() -
                                datetime.timedelta(hours=24)).delete()

    return
