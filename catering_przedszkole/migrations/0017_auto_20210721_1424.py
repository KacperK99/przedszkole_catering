# Generated by Django 2.2b1 on 2021-07-21 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catering_przedszkole', '0016_auto_20210721_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danie',
            name='zdjecie',
            field=models.ImageField(blank=True, default='image/brak_zdjecia.png', upload_to='image'),
        ),
    ]
