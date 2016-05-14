# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monthly_summary', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('last_checked', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('username', models.CharField(max_length=2000)),
                ('password', models.CharField(max_length=2000)),
                ('first_name', models.CharField(max_length=2000, null=True, blank=True)),
                ('last_name', models.CharField(max_length=2000, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=2000, null=True, blank=True)),
                ('owner_reimbursement_rate', models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('location', models.CharField(max_length=2000, null=True, blank=True)),
                ('date_of_reservation', models.DateField(null=True, blank=True)),
                ('number_of_nights', models.IntegerField(null=True, blank=True)),
                ('unit_size', models.CharField(max_length=2000, null=True, blank=True)),
                ('confirmation_number', models.CharField(max_length=2000)),
                ('points_required_for_reservation', models.IntegerField(null=True, blank=True)),
                ('is_buyer_lined_up', models.IntegerField(null=True, blank=True, choices=[(1, 'True'), (0, 'False')])),
                ('amount_paid', models.FloatField(null=True, blank=True)),
                ('date_booked', models.DateField(null=True, blank=True)),
                ('upgrade_status', models.CharField(max_length=2000, null=True, blank=True)),
                ('guest_certificate', models.CharField(max_length=2000, null=True, blank=True)),
                ('touched', models.DateField(null=True, default=None, blank=True)),
                ('touched_bool', models.NullBooleanField(default=None)),
                ('canceled', models.NullBooleanField(default=None)),
                ('fk_monthly_report', models.ForeignKey(default=None, to='monthly_summary.MonthlyReport', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True)),
                ('fk_owner', models.ForeignKey(to='reservation_manager.Owner', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True)),
            ],
        ),
    ]
