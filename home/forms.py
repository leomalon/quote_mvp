from django import forms
from django.contrib.auth import authenticate

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Correo electrónico',
            'class': 'input-field'
        })
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'input-field'
        })
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email/password.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        return self.cleaned_data

    def get_user(self):
        return self.user_cache



