# Generated by Django 4.2.7 on 2023-11-15 23:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("comentarios", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="comentario",
            name="timestamp",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]