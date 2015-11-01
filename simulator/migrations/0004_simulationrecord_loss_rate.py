# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0003_simulationrecord_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulationrecord',
            name='loss_rate',
            field=models.FloatField(default=0, verbose_name=b'\xe4\xb8\xa2\xe5\x8c\x85\xe7\x8e\x87'),
        ),
    ]
