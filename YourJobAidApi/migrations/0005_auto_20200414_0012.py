# Generated by Django 3.0.4 on 2020-04-13 18:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('YourJobAidApi', '0004_auto_20200414_0002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ManyToManyField(default=1, to=settings.AUTH_USER_MODEL),
        ),
    ]
