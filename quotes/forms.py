from django import forms
from .models import Quote, Cliente

class QuoteForm(forms.ModelForm):
    #Here we replicate the fields of Cliente that we do not have in the model Quote.
    contacto = forms.CharField(label="Contacto", max_length=255)
    email_contacto = forms.EmailField(label="Correo del contacto", required=False)
    cliente_empresa = forms.CharField(label="Empresa", max_length=255, required=False)

    class Meta:
        model = Quote
        fields = ['nombre', 'description', 'contacto', 'email_contacto', 'cliente_empresa', 'estado','precio', 'pdf'] #This is for the form fields objects.


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  #initializes the form fields, binds data if passed and sets up widgets.
        contactos = Cliente.objects.values_list('contacto', flat=True) #returns a list not tuple
        self.fields['contacto'].widget = forms.TextInput(attrs={ #We override the default widget for this field with TextInput with attributes.
            'list': 'contacto_list',
            'autocomplete': 'off'
        })
        self.contacto_options = contactos #This attaches a contact_options attribute to the form instance
        
        self.fields['nombre'].widget = forms.TextInput(attrs={
            'placeholder': 'Título cotización',
            'class': 'input-field'
        })
        self.fields['description'].widget = forms.Textarea(attrs={
            'placeholder': 'Descripción de la cotización',
            'class': 'description-textarea'
        })
        self.fields['contacto'].widget = forms.TextInput(attrs={
            'placeholder': 'Contacto',
            'class': 'input-field'
        })

        self.fields['email_contacto'].widget = forms.TextInput(attrs={
            'placeholder': 'Correo del contacto',
            'class': 'input-field'
        })
        self.fields['cliente_empresa'].widget = forms.TextInput(attrs={
            'placeholder': 'Empresa',
            'class': 'input-field'
        })
        self.fields['precio'].widget = forms.TextInput(attrs={
            'placeholder': 'Precio (S/.)',
            'class': 'input-field'
        })
        self.fields['pdf'].widget = forms.FileInput(attrs={ #Here avoid using ClearableFileInput to not show "Current" and "Change"
            'class': 'custom-file-input',
            'style': 'display: none;',  # hide native input
            'id': 'id_pdf'  # ensure it has this id
        })


        #We define this inside "__init__", because it will run everytime a form is initiated so its dynamic.
