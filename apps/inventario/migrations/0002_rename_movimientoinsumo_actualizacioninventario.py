# Generated by Django 5.2.3 on 2025-07-15 06:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("inventario", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="MovimientoInsumo",
            new_name="ActualizacionInventario",
        ),
    ]
