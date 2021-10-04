# Generated by Django 2.2.23 on 2021-09-29 22:19

from django.db import migrations, models
import usaspending_api.common.custom_django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0084_auto_20210805_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionfabs',
            name='funding_opportunity_goals',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transactionfabs',
            name='funding_opportunity_number',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transactionfabs',
            name='indirect_federal_sharing',
            field=usaspending_api.common.custom_django_fields.NumericField(blank=True, null=True),
        ),
    ]
