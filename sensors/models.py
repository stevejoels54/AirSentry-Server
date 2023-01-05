from django.db import models

# Create your models here.


class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=200)
    device_location = models.CharField(max_length=200)
    device_lat = models.FloatField()
    device_long = models.FloatField()
    device_status = models.CharField(max_length=200)

    def __str__(self):
        return self.device_id


class Reading(models.Model):
    reading_id = models.AutoField(primary_key=True)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    air = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('timestamp', 'reading_id'), )

    def __str__(self):
        return self.reading_id


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=200)
    notification_message = models.CharField(max_length=200)
    notification_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_id