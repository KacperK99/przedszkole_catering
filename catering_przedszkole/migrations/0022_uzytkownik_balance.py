# Generated by Django 2.2b1 on 2021-09-20 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catering_przedszkole', '0021_auto_20210721_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='uzytkownik',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]