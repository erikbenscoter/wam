# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_manager', '0011_reservation_canceled'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('last_checked', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
