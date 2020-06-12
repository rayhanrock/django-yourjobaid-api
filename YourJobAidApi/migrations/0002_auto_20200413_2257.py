# Generated by Django 3.0.4 on 2020-04-13 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('YourJobAidApi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='username',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
