# Generated by Django 5.0.6 on 2024-06-25 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apps', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='user',
            new_name='peoples',
        ),
    ]
