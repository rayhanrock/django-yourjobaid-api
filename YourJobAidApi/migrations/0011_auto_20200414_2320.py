# Generated by Django 3.0.4 on 2020-04-14 17:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('YourJobAidApi', '0010_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category_identying_slug',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=300, unique=True),
        ),
    ]
