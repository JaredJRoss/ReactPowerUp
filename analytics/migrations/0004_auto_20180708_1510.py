# Generated by Django 2.0.2 on 2018-07-08 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_daycount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daycount',
            name='Date',
            field=models.DateTimeField(verbose_name='Date'),
        ),
    ]