# Generated by Django 2.0.2 on 2018-07-08 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_auto_20180331_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(verbose_name='Date')),
                ('Count', models.IntegerField(verbose_name='Count')),
            ],
        ),
    ]
