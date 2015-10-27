# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VehicleDataORM', '0004_road_road_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimulationRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frame_id', models.IntegerField(default=0, verbose_name=b'\xe5\xb8\xa7id')),
                ('lane_pos', models.IntegerField(default=0, verbose_name=b'\xe8\xbd\xa6\xe9\x81\x93\xe4\xbd\x8d\xe7\xbd\xae')),
                ('estimate_value', models.FloatField(default=0, verbose_name=b'\xe4\xbc\xb0\xe8\xae\xa1\xe5\x80\xbc')),
                ('real_value', models.FloatField(default=0, verbose_name=b'\xe5\xae\x9e\xe9\x99\x85\xe5\x80\xbc')),
                ('estimation_method', models.CharField(max_length=50, verbose_name=b'\xe4\xbc\xb0\xe8\xae\xa1\xe6\x96\xb9\xe6\xb3\x95\xe7\x9a\x84\xe5\x90\x8d\xe7\xa7\xb0')),
                ('z', models.FloatField(default=300, verbose_name=b'\xe9\x80\x9a\xe4\xbf\xa1\xe8\xb7\x9d\xe7\xa6\xbb')),
                ('road', models.ForeignKey(verbose_name=b'\xe5\xaf\xb9\xe5\xba\x94\xe7\x9a\x84spacing\xe8\xa1\xa8\xe5\x8d\x95', to='VehicleDataORM.Road')),
            ],
        ),
    ]
