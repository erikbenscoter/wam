# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_manager', '0008_auto_20160409_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='fk_monthly_report',
            field=models.ForeignKey(default=None, blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='monthly_summary.MonthlyReport'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='fk_owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='reservation_manager.Owner'),
        ),
    ]
