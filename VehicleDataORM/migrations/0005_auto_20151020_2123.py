# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VehicleDataORM', '0004_road_road_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='frame_id',
            field=models.IntegerField(default=0, verbose_name='\u5e27id', db_index=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='local_y',
            field=models.FloatField(default=0, verbose_name='y', db_index=True),
        ),
    ]
