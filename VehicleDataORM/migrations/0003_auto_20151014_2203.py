# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VehicleDataORM', '0002_auto_20151013_0424'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ('frame_id',)},
        ),
        migrations.AddField(
            model_name='record',
            name='processed',
            field=models.BooleanField(default=False, help_text=b'\xe8\xbf\x99\xe6\x9d\xa1\xe8\xae\xb0\xe5\xbd\x95\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe7\xbb\x8f\xe8\xa2\xab\xe5\xa4\x84\xe7\x90\x86\xe4\xba\x86'),
        ),
    ]
