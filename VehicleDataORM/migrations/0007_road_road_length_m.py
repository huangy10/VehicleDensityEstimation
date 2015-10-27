# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VehicleDataORM', '0006_auto_20151023_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='road',
            name='road_length_m',
            field=models.FloatField(default=0),
        ),
    ]
