# Generated by Django 2.2b1 on 2021-07-02 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catering_przedszkole', '0009_auto_20210702_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zestaw_dan',
            name='ilosc_zestawow',
        ),
        migrations.AddField(
            model_name='zamowienie',
            name='ilosc_zestawow',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=5),
        ),
    ]
