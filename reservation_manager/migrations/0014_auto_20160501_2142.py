# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_manager', '0013_auto_20160501_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationsettings',
            name='last_checked',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
