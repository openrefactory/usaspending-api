# Generated by Django 2.2.11 on 2020-04-02 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200320_1307'),
    ]

    operations = [
        migrations.RunSQL(sql=["drop function if exists corrected_cgac"]),
    ]
