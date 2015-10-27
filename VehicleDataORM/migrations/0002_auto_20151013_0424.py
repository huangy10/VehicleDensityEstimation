# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VehicleDataORM', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='road',
            field=models.ForeignKey(default=None, to='VehicleDataORM.Road'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicle',
            name='v_id',
            field=models.IntegerField(default=0, verbose_name='\u6587\u4ef6\u4e2d\u5b9a\u4e49\u7684id'),
        ),
    ]
