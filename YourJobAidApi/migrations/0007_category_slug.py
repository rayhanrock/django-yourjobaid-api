# Generated by Django 3.0.4 on 2020-04-14 15:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('YourJobAidApi', '0006_auto_20200414_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=300, null=True),
        ),
    ]