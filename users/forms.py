from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from collections import OrderedDict

CustomUser = get_user_model()

class CustomUserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput())

    def __init__(self, *args, social_email=None, **kwargs):
        super().__init__(*args, **kwargs)
        if social_email:
            self.fields['email'].initial = social_email
            self.fields['email'].disabled = True  # Prevent editing

        self.social_email = social_email

        # Dynamically add fields only for non-social users
        if not self.instance.pk:
            self.fields['first_name'] = forms.CharField(label='Nombre', max_length=255,validators=[MinLengthValidator(3, 'Ingresa un nombre válido')])
            self.fields['last_name'] = forms.CharField(label='Apellido', max_length=255,validators=[MinLengthValidator(3, 'Ingresa un apellido válido')])
            self.fields['email'].required = True
            self.fields['password1'].required = True
            self.fields['password2'].required = True
            
            reordered = OrderedDict()
            # Reorder fields to place first_name and last_name after email
            for field_name in self.fields:
                reordered[field_name] = self.fields[field_name]
                if field_name == "email":
                    reordered['first_name'] = self.fields['first_name']
                    reordered['last_name'] = self.fields['last_name']
            # Add any remaining fields not yet in reordered
            for field_name in self.fields:
                if field_name not in reordered:
                    reordered[field_name] = self.fields[field_name]
            self.fields = reordered


        self.fields['email'].error_messages = {
            'required': 'El correo electrónico es obligatorio.',
            'invalid': 'Introduce un correo electrónico válido.',
        }
        self.fields['first_name'].error_messages = {
            'required': 'El nombre es obligatorio.'
        }
        self.fields['last_name'].error_messages = {
            'required': 'El apellido es obligatorio.'
        }
        self.fields['company'].error_messages = {
            'required': 'El nombre de Empresa es obligatorio.'
        }
        self.fields['rol'].error_messages = {
            'required': 'El puesto es obligatorio.'
        }
        self.fields['ruc'].error_messages = {
            'required': 'El RUC es obligatorio'
        }
        self.fields['password1'].error_messages = {
            'required': 'Este campo es obligatorio'
        }
        self.fields['password2'].error_messages = {
            'required': 'Este campo es obligatorio'
        }


    class Meta:
        model = CustomUser
        fields = ['email', 'telefono_movil','company', 'ruc', 'rol']  # first/last name added dynamically

    def clean(self):
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get("password1")
        pwd2 = cleaned_data.get("password2")

        if not self.instance.pk:  # New user
            if not pwd1 or not pwd2:
                raise ValidationError("Debes ingresar una contraseña.")
            if pwd1 != pwd2:
                raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # For new users only (manual or social completing profile)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user





