# Generated by Django 5.1.7 on 2025-07-27 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_weightclassification_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocationdetails',
            name='allocated_bags',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
