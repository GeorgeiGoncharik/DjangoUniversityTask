# Generated by Django 2.1.15 on 2020-05-03 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='measure_type',
            field=models.CharField(max_length=20, verbose_name='Единица измерения'),
        ),
    ]
