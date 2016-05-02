# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_manager', '0010_remove_owner_avail_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='canceled',
            field=models.NullBooleanField(default=None),
        ),
    ]
