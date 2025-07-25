# Generated by Django 4.2.12 on 2025-06-28 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("components", "0012_alter_manufacturer_component_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="case",
            name="side_panel_window",
            field=models.BooleanField(default=False, verbose_name="Боковое окно"),
        ),
        migrations.AddField(
            model_name="cooler",
            name="rgb",
            field=models.BooleanField(default=False, verbose_name="RGB подсветка"),
        ),
        migrations.AddField(
            model_name="cpu",
            name="integrated_graphics",
            field=models.BooleanField(
                default=False, verbose_name="Интегрированная графика"
            ),
        ),
        migrations.AddField(
            model_name="gpu",
            name="ray_tracing",
            field=models.BooleanField(
                default=False, verbose_name="Поддержка Ray Tracing"
            ),
        ),
        migrations.AddField(
            model_name="motherboard",
            name="wifi",
            field=models.BooleanField(default=False, verbose_name="Wi-Fi"),
        ),
        migrations.AddField(
            model_name="psu",
            name="modular",
            field=models.BooleanField(default=False, verbose_name="Модульный"),
        ),
        migrations.AddField(
            model_name="ram",
            name="rgb",
            field=models.BooleanField(default=False, verbose_name="RGB подсветка"),
        ),
        migrations.AddField(
            model_name="storage",
            name="nvme",
            field=models.BooleanField(default=False, verbose_name="NVMe Support"),
        ),
    ]
