# Generated by Django 5.2 on 2025-05-11 23:26

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cliente",
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
                ("contacto", models.CharField(max_length=255, verbose_name="Contacto")),
                (
                    "cliente_empresa",
                    models.CharField(max_length=255, verbose_name="Empresa"),
                ),
                (
                    "email_contacto",
                    models.EmailField(
                        max_length=254,
                        validators=[
                            django.core.validators.EmailValidator(
                                message="Ingrese un correo válido."
                            )
                        ],
                        verbose_name="Correo del contacto",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Quote",
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
                (
                    "nombre",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, "Nombre debe ser mayor a 2 letras"
                            )
                        ],
                        verbose_name="Nombre de la cotización",
                    ),
                ),
                (
                    "description",
                    models.TextField(verbose_name="Breve descripción de la cotización"),
                ),
                (
                    "fecha_creacion",
                    models.DateTimeField(auto_now_add=True, verbose_name="Fecha"),
                ),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("Pendiente", "Pendiente"),
                            ("En OC", "En OC"),
                            ("Ejecución", "Ejecución"),
                            ("Terminado", "Terminado"),
                            ("Facturado", "Facturado"),
                            ("Cancelado", "Cancelado"),
                        ],
                        default="Pendiente",
                        max_length=20,
                        verbose_name="Estado",
                    ),
                ),
                (
                    "pdf",
                    models.FileField(
                        upload_to="quotes_pdfs/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["pdf"]
                            )
                        ],
                        verbose_name="Archivo PDF",
                    ),
                ),
                (
                    "cotizacion_id",
                    models.CharField(
                        blank=True,
                        editable=False,
                        max_length=55,
                        verbose_name="Cotización ID",
                    ),
                ),
                (
                    "cliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quotes.cliente"
                    ),
                ),
            ],
        ),
    ]
