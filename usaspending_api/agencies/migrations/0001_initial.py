# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-29 18:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('references', '0030_auto_20190823_2139'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=None,
            state_operations=[
                migrations.CreateModel(
                    name='CGAC',
                    fields=[
                        ('cgac_code', models.TextField(primary_key=True, serialize=False)),
                        ('agency_name', models.TextField()),
                        ('agency_abbreviation', models.TextField(blank=True, null=True)),
                    ],
                    options={
                        'db_table': 'cgac',
                    },
                ),
            ],
        ),
        migrations.CreateModel(
            name='FREC',
            fields=[
                ('frec_code', models.TextField(primary_key=True, serialize=False)),
                ('agency_name', models.TextField()),
                ('agency_abbreviation', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'frec',
            },
        ),
        migrations.CreateModel(
            name='RawAgency',
            fields=[
                ('row_number', models.IntegerField(primary_key=True, serialize=False)),
                ('cgac_agency_code', models.TextField(blank=True, null=True)),
                ('agency_name', models.TextField(blank=True, null=True)),
                ('agency_abbreviation', models.TextField(blank=True, null=True)),
                ('frec', models.TextField(blank=True, null=True)),
                ('frec_entity_description', models.TextField(blank=True, null=True)),
                ('frec_abbreviation', models.TextField(blank=True, null=True)),
                ('subtier_code', models.TextField(blank=True, null=True)),
                ('subtier_name', models.TextField(blank=True, null=True)),
                ('subtier_abbreviation', models.TextField(blank=True, null=True)),
                ('admin_org_name', models.TextField(blank=True, null=True)),
                ('admin_org', models.TextField(blank=True, null=True)),
                ('toptier_flag', models.BooleanField()),
                ('is_frec', models.BooleanField()),
                ('frec_cgac_association', models.BooleanField()),
                ('user_selectable_on_usaspending_gov', models.BooleanField()),
                ('mission', models.TextField(blank=True, null=True)),
                ('website', models.TextField(blank=True, null=True)),
                ('congressional_justification', models.TextField(blank=True, null=True)),
                ('icon_filename', models.TextField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'raw_agency',
            },
        ),
        migrations.CreateModel(
            name='SubtierAgency',
            fields=[
                ('subtier_code', models.TextField(primary_key=True, serialize=False)),
                ('agency_name', models.TextField()),
                ('agency_abbreviation', models.TextField(blank=True, null=True)),
                ('is_toptier', models.BooleanField()),
            ],
            options={
                'db_table': 'subtier_agency_new',
            },
        ),
        migrations.CreateModel(
            name='ToptierAgency',
            fields=[
                ('toptier_code', models.TextField(primary_key=True, serialize=False)),
                ('agency_name', models.TextField()),
                ('agency_abbreviation', models.TextField(blank=True, null=True)),
                ('mission', models.TextField(blank=True, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('congressional_justification', models.URLField(blank=True, null=True)),
                ('icon_filename', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'toptier_agency_new',
            },
        ),
        migrations.AddField(
            model_name='subtieragency',
            name='toptier',
            field=models.ForeignKey(db_column='toptier_code', on_delete=django.db.models.deletion.CASCADE, to='agencies.ToptierAgency'),
        ),
    ]
