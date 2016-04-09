# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyReport',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('check_number', models.CharField(max_length=2000, null=True, blank=True)),
                ('amount_paid', models.FloatField(default=0.0)),
                ('date_paid', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
        ),
    ]
