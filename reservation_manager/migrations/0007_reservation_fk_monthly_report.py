# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monthly_summary', '0001_initial'),
        ('reservation_manager', '0006_remove_reservation_fk_monthly_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='fk_monthly_report',
            field=models.ForeignKey(blank=True, null=True, to='monthly_summary.MonthlyReport'),
        ),
    ]
