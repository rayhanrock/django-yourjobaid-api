# Generated by Django 3.0.4 on 2020-04-15 17:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('YourJobAidApi', '0016_auto_20200415_0136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category_identifying_slug',
        ),
    ]