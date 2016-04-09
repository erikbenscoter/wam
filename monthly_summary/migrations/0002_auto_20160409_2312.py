# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monthly_summary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyreport',
            name='date_paid',
            field=models.DateTimeField(null=True, default=None, blank=True),
        ),
    ]
