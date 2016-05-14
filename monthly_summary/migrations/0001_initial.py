# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('check_number', models.CharField(max_length=2000, null=True, blank=True)),
                ('amount_paid', models.FloatField(default=0.0)),
                ('date_paid', models.DateTimeField(default=None, null=True, blank=True)),
            ],
        ),
    ]
