# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulationrecord',
            name='extra_params',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xe9\xa2\x9d\xe5\xa4\x96\xe5\x8f\x82\xe6\x95\xb0\xe4\xbf\xa1\xe6\x81\xaf'),
        ),
    ]
