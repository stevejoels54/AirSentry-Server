from rest_framework import serializers
from .models import Reading, Device, Notification


class ReadingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reading
        fields = ('reading_id', 'device_id', 'air', 'temperature', 'humidity',
                  'timestamp')

    def create(self, validated_data):
        return Reading.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.reading_id = validated_data.get('reading_id',
                                                 instance.reading_id)
        instance.device_id = validated_data.get('device_id',
                                                instance.device_id)
        instance.air = validated_data.get('air', instance.air)
        instance.temperature = validated_data.get('temperature',
                                                  instance.temperature)
        instance.humidity = validated_data.get('humidity', instance.humidity)
        instance.timestamp = validated_data.get('timestamp',
                                                instance.timestamp)
        instance.save()
        return instance


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ('device_id', 'device_name', 'device_type', 'device_location',
                  'device_lat', 'device_long', 'device_status')

    def create(self, validated_data):
        return Device.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.device_id = validated_data.get('device_id',
                                                instance.device_id)
        instance.device_name = validated_data.get('device_name',
                                                  instance.device_name)
        instance.device_type = validated_data.get('device_type',
                                                  instance.device_type)
        instance.device_location = validated_data.get('device_location',
                                                      instance.device_location)
        instance.device_lat = validated_data.get('device_lat',
                                                 instance.device_lat)
        instance.device_long = validated_data.get('device_long',
                                                  instance.device_long)
        instance.device_status = validated_data.get('device_status',
                                                    instance.device_status)
        instance.save()
        return instance


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('notification_id', 'device_id', 'notification_type',
                  'notification_message', 'notification_timestamp')

    def create(self, validated_data):
        return Notification.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.notification_id = validated_data.get('notification_id',
                                                      instance.notification_id)
        instance.device_id = validated_data.get('device_id',
                                                instance.device_id)
        instance.notification_type = validated_data.get(
            'notification_type', instance.notification_type)
        instance.notification_message = validated_data.get(
            'notification_message', instance.notification_message)
        instance.notification_timestamp = validated_data.get(
            'notification_timestamp', instance.notification_timestamp)
        instance.save()
        return instance
