# Generated by Django 3.0.4 on 2020-04-20 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YourJobAidApi', '0027_auto_20200420_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(default='jobaid_default_post_pic/yourjobaid.jpg', upload_to='jobs/%Y/%M/%D'),
        ),
    ]
