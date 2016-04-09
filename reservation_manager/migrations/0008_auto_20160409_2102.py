# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_manager', '0007_reservation_fk_monthly_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='fk_monthly_report',
            field=models.ForeignKey(null=True, blank=True, default=None, to='monthly_summary.MonthlyReport'),
        ),
    ]
