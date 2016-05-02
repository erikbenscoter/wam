# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_manager', '0012_applicationsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='touched_bool',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='touched',
            field=models.DateField(default=None, blank=True, null=True),
        ),
    ]
