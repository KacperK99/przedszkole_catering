# Generated by Django 2.2b1 on 2021-07-02 14:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catering_przedszkole', '0008_zestaw_dan_ilosc_zestawow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zamowienie',
            name='data_zamowienia',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
