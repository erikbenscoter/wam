# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_manager', '0005_auto_20160409_0017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='fk_monthly_report',
        ),
    ]
