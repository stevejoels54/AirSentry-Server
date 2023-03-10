# Generated by Django 4.1.4 on 2023-01-02 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0003_alter_reading_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notification_id', models.AutoField(primary_key=True, serialize=False)),
                ('notification_type', models.CharField(max_length=200)),
                ('notification_message', models.CharField(max_length=200)),
                ('notification_timestamp', models.DateTimeField(auto_now_add=True)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sensors.device')),
            ],
        ),
    ]
