# Generated by Django 3.0.4 on 2020-04-14 19:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('YourJobAidApi', '0015_post_category_read_only'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='category_identying_slug',
            new_name='category_identifying_slug',
        ),
    ]