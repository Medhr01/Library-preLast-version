# Generated by Django 5.0.4 on 2024-05-14 14:14

import Lib_sys.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lib_sys', '0009_alter_bouquin_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprunt',
            name='Client',
            field=models.ForeignKey(on_delete=models.SET(Lib_sys.models.Client), to='Lib_sys.client'),
        ),
    ]
