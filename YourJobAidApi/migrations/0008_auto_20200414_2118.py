# Generated by Django 3.0.4 on 2020-04-14 15:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('YourJobAidApi', '0007_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=300, null=True, unique=True),
        ),
    ]