# Generated by Django 2.2b1 on 2021-07-07 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catering_przedszkole', '0014_auto_20210706_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='zamowienie',
            name='czy_anulowano',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='zamowienie',
            name='powod_anulowania',
            field=models.TextField(blank=True, null=True),
        ),
    ]
