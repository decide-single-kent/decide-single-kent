# Generated by Django 4.1 on 2023-12-10 20:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comentario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("autor", models.CharField(max_length=100)),
                ("texto", models.TextField()),
                ("fecha_publicacion", models.DateTimeField(auto_now_add=True)),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                ("votos_positivos", models.IntegerField(default=0)),
                ("votos_negativos", models.IntegerField(default=0)),
            ],
        ),
    ]
