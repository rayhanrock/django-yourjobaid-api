# Generated by Django 3.0.4 on 2020-04-14 15:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('YourJobAidApi', '0009_auto_20200414_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=300, null=True, unique=True),
        ),
    ]