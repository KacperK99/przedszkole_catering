# Generated by Django 2.2b1 on 2021-07-01 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catering_przedszkole', '0006_auto_20210701_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zestaw',
            name='cena_zestawu',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
