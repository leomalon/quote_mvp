from django.db import models
from django.core.validators import MinLengthValidator, FileExtensionValidator, EmailValidator
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
import os

    
class Cliente(models.Model):
    contacto = models.CharField("Contacto", max_length=255)
    cliente_empresa = models.CharField("Empresa", max_length=255,null=False,blank=False)
    email_contacto = models.EmailField(
    "Correo del contacto",
    validators=[EmailValidator(message="Ingrese un correo válido.")],
    null=False,
    blank=False)
    usuario_cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.contacto
    

class Quote(models.Model):
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En OC', 'En OC'),
        ('Ejecución', 'Ejecución'),
        ('Terminado', 'Terminado'),
        ('Facturado', 'Facturado'),
        ('Cancelado','Cancelado')
    ]

    #The 'id' field is auto-generated

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    nombre = models.CharField("Nombre de la cotización", max_length=255, 
                              validators=[MinLengthValidator(2,"Ingresar un nombre de cotización mayor a 2 caracteres")],
                              null=False,
                              blank=False)
    description = models.TextField("Breve descripción de la cotización",validators=[MinLengthValidator(5,"Ingresar una descripción mayor a 5 caracteres")])
    fecha_creacion = models.DateTimeField("Fecha", auto_now_add=True)
    estado = models.CharField(
        "Estado",
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pendiente',
        null=False,
        blank=False
    )

    pdf = models.FileField(
        "Archivo PDF",
        upload_to='quotes_pdfs/', #Defines a directory "MEDIA_ROOT" where files will be stored
        validators=[FileExtensionValidator(allowed_extensions=['pdf'],message='Solo se permiten archivos en formato PDF.')],
        blank=False,
        null=False
    )


    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False, blank=False) #Every quote related with a "Cliente"

    cotizacion_id = models.CharField("Cotización ID", max_length=55,blank=True, editable=False)
    precio = models.DecimalField(
        "Precio",
        max_digits=12,  # e.g., 999,999,999.99
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=False,
        blank=False
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        # For updates, get the old instance before saving
        if not is_new:
            try:
                old_instance = Quote.objects.get(pk=self.pk)
                if old_instance.pdf and old_instance.pdf != self.pdf:
                    if os.path.isfile(old_instance.pdf.path):
                        os.remove(old_instance.pdf.path)
            except Quote.DoesNotExist:
                pass  # Should not occur

        # Save the instance
        super().save(*args, **kwargs)

        # For new instances, set cotizacion_id after the initial save
        if is_new:
            year_month = self.fecha_creacion.strftime('%Y_%m')
            company = self.usuario.company.upper()
            self.cotizacion_id = f"{company}_{year_month}_{self.id}"
            super().save(update_fields=['cotizacion_id'])


    def delete(self, *args, **kwargs):
        # Delete the file from the storage first
        if self.pdf and os.path.isfile(self.pdf.path):
            os.remove(self.pdf.path)
        # Call the superclass delete method
        super().delete(*args, **kwargs)


    def __str__(self):
        return self.nombre