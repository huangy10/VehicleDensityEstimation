# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VehicleDataORM', '0005_auto_20151020_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='local_y_m',
            field=models.FloatField(default=0, verbose_name='y_in_meters', db_index=True),
        ),
        migrations.AddField(
            model_name='record',
            name='spacing_m',
            field=models.FloatField(default=0, verbose_name='\u4e0e\u524d\u8f66\u7684\u8ddd\u79bb_in_meters'),
        ),
    ]
