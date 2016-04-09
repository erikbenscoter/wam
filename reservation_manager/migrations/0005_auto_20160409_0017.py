# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_manager', '0004_auto_20160409_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='fk_monthly_report',
            field=models.ForeignKey(null=True, to='monthly_summary.MonthlyReport', blank=True),
        ),
    ]
