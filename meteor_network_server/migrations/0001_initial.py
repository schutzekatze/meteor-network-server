# Generated by Django 2.1.1 on 2018-09-18 21:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import meteor_network_server.stations.stations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrationNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='', max_length=4096)),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Test Component', max_length=64)),
                ('old', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(default='', max_length=512)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meteor_network_server.Component')),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default='', max_length=128)),
                ('value', models.CharField(default='', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='MeasurementBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meteor_network_server.Component')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Test Person', max_length=64)),
                ('phone', models.CharField(default='', max_length=64)),
                ('email', models.CharField(default='', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network_id', models.CharField(max_length=64)),
                ('name', models.CharField(default='Test Station', max_length=64)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('height', models.FloatField(default=0.0)),
                ('comment', models.TextField(default='', max_length=512)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved', models.BooleanField(default=False)),
                ('maintainers', models.ManyToManyField(to='meteor_network_server.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Test Status', max_length=64)),
                ('color', models.CharField(default='#00CC00', max_length=16)),
                ('severity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='StatusRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expression', models.CharField(max_length=256)),
                ('message', models.CharField(max_length=128)),
                ('status', models.ForeignKey(default=meteor_network_server.stations.stations.get_status_rule_broken, on_delete=django.db.models.deletion.CASCADE, to='meteor_network_server.Status')),
            ],
        ),
        migrations.AddField(
            model_name='station',
            name='status',
            field=models.ForeignKey(default=meteor_network_server.stations.stations.get_status_default, on_delete=django.db.models.deletion.SET_DEFAULT, to='meteor_network_server.Status'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meteor_network_server.MeasurementBatch'),
        ),
        migrations.AddField(
            model_name='component',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meteor_network_server.Station'),
        ),
    ]
