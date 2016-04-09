# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monthly_summary', '0001_initial'),
        ('reservation_manager', '0002_auto_20160325_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='fk_monthly_report',
            field=models.ForeignKey(default='', to='monthly_summary.MonthlyReport'),
            preserve_default=False,
        ),
    ]
