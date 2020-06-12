# Generated by Django 3.0.4 on 2020-04-20 09:17

import YourJobAidApi.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YourJobAidApi', '0026_auto_20200420_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(default='default_pro_pic/dp.png', upload_to='jobs/%Y/%M/%D'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(default='default_pro_pic/dp.png', upload_to=YourJobAidApi.models.user_profile_picture_directory_path),
        ),
    ]
