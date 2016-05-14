# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owners_Points_Status',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('Travel_From', models.DateField(blank=True, null=True)),
                ('Expiration', models.DateField(blank=True, null=True)),
                ('Points_Description', models.CharField(max_length=20, null=True, blank=True)),
                ('Points_Available', models.IntegerField(blank=True, null=True)),
                ('Housekeeping_Available', models.IntegerField(blank=True, null=True)),
                ('fk_owner', models.ForeignKey(to='reservation_manager.Owner')),
            ],
        ),
    ]
