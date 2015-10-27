# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0002_simulationrecord_extra_params'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulationrecord',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 21, 50, 55, 815431), auto_now_add=True),
            preserve_default=False,
        ),
    ]
