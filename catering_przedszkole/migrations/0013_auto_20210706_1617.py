# Generated by Django 2.2b1 on 2021-07-06 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catering_przedszkole', '0012_auto_20210702_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zamowienie',
            name='zestaw',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='catering_przedszkole.Zestaw'),
        ),
    ]
