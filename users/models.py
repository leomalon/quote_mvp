from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo electrónico es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    first_name = models.CharField("Nombre", max_length=255)
    last_name = models.CharField("Apellido", max_length=255)
    email = models.EmailField(unique=True, verbose_name='Correo electrónico') 
    telefono_movil = models.CharField(max_length=20, blank=True)
    ruc = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^\d{11}$', message='El RUC debe tener exactamente 11 dígitos.')],
        unique=True,
        verbose_name='RUC',
        blank=True,
        null=True
    )
    company = models.CharField(max_length=255, verbose_name='Empresa')
    rol = models.CharField(max_length=255, verbose_name="Puesto",validators=[MinLengthValidator(2, 'Debes ingresar más de 2 caracteres')])

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.company})"
