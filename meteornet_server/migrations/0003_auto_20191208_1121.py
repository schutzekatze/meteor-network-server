# Generated by Django 2.2.6 on 2019-12-08 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meteornet_server', '0002_auto_20191130_0817'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StatusRule',
            new_name='StatusWarning',
        ),
    ]
