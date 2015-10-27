# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VehicleDataORM', '0003_auto_20151014_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='road',
            name='road_length',
            field=models.FloatField(default=0),
        ),
    ]
