# Generated by Django 2.2b1 on 2021-07-21 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catering_przedszkole', '0020_auto_20210721_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danie',
            name='zdjecie',
            field=models.ImageField(blank=True, max_length=300, upload_to='image'),
        ),
    ]
