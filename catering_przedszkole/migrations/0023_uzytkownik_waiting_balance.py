# Generated by Django 2.2b1 on 2021-09-20 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catering_przedszkole', '0022_uzytkownik_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='uzytkownik',
            name='waiting_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
