# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description_file', models.FilePathField(null=True)),
                ('frame_id', models.IntegerField(default=0, verbose_name='\u5e27id')),
                ('global_time', models.BigIntegerField(default=0, verbose_name='\u5168\u5c40\u65f6\u95f4')),
                ('local_x', models.FloatField(default=0, verbose_name='x')),
                ('local_y', models.FloatField(default=0, verbose_name='y')),
                ('global_x', models.FloatField(default=0, verbose_name='\u5168\u5c40\u5750\u6807x')),
                ('global_y', models.FloatField(default=0, verbose_name='\u5168\u5c40\u5750\u6807y')),
                ('velocity', models.FloatField(default=0, verbose_name='\u6c7d\u8f66\u901f\u5ea6')),
                ('acceleration', models.FloatField(default=0, verbose_name='\u6c7d\u8f66\u52a0\u901f\u5ea6')),
                ('lane_pos', models.IntegerField(default=0, verbose_name='\u8f66\u9053\u4f4d\u7f6e')),
                ('spacing', models.FloatField(default=0, verbose_name='\u4e0e\u524d\u8f66\u7684\u8ddd\u79bb')),
                ('headway', models.FloatField(default=0, help_text='\n        Headway provides the time to travel from the front-center of a vehicle (at the speed of the vehicle) to the\n        front-center of the preceding vehicle. A headway value of 9999.99 means that the vehicle is traveling at zero\n        speed (congested conditions).\n    ')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Road',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u9053\u8def\u540d\u79f0')),
                ('description', models.TextField(max_length=255, verbose_name='\u9053\u8def\u4fe1\u606f\u63cf\u8ff0')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('width', models.FloatField(default=0, verbose_name='\u8f66\u8f86\u5bbd\u5ea6')),
                ('length', models.FloatField(default=0, verbose_name='\u8f66\u8f86\u957f\u5ea6')),
                ('name', models.CharField(default='', max_length=255, verbose_name='\u8f66\u8f86\u540d\u79f0')),
                ('vehicle_class', models.IntegerField(default=1, choices=[(1, b'motorcycle'), (2, b'auto'), (3, b'trunk')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='record',
            name='following_vehicle',
            field=models.ForeignKey(related_name='+', to='VehicleDataORM.Vehicle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='record',
            name='preceding_vehicle',
            field=models.ForeignKey(related_name='+', to='VehicleDataORM.Vehicle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='record',
            name='road',
            field=models.ForeignKey(to='VehicleDataORM.Road'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='record',
            name='vehicle',
            field=models.ForeignKey(to='VehicleDataORM.Vehicle'),
            preserve_default=True,
        ),
    ]
