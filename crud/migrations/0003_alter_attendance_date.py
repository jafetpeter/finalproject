# Generated by Django 4.2.8 on 2025-06-04 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0002_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(),
        ),
    ]
