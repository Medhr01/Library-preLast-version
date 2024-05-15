# Generated by Django 5.0.4 on 2024-05-15 01:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lib_sys', '0011_alter_emprunt_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprunt',
            name='client_info',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='emprunt',
            name='exemplaire_info',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='client',
            name='Statut',
            field=models.CharField(default='Actif', max_length=50),
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='Client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Lib_sys.client'),
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='Exemplaire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Lib_sys.exemplaire'),
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='bibliothecaire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]