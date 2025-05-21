from django.shortcuts import render, get_object_or_404,redirect
from .owner import OwnerListView,OwnerDetailView,OwnerDeleteView, OwnerUpdateView,OwnerCreateView
from .models import Quote, Cliente
from django.urls import reverse_lazy
from .forms import QuoteForm
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.db import models


from django.db.models import Q

class QuoteListView(OwnerListView):
    model = Quote
    # By convention:
    template_name = "quotes/quote_list.html"
    context_object_name = "quote_list" #This is how we override the context variable name
    #model_list will be the context variable 
    #quote_list is the list of objects
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs) #Creates a dictionary with default variables like "quote_list":Queryset of model objects
        context['app_name'] = settings.APP_NAME
        context['usuario'] = self.request.user
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                models.Q(nombre__icontains=query) |
                models.Q(cliente__cliente_empresa__icontains=query) |
                models.Q(estado__icontains=query) |
                models.Q(cotizacion_id__icontains=query) |
                models.Q(fecha_creacion__icontains=query)
            )
        return queryset
    

class QuoteCreateView(OwnerCreateView):
    model = Quote #Django uses this to automatically build the form (ModelForm)
    form_class = QuoteForm
    template_name = 'quotes/quote_form.html'
    success_url = reverse_lazy('quotes:quotes_all')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #This is to get the default context {'form':form}
        contactos = Cliente.objects.all().values('contacto', 'email_contacto', 'cliente_empresa') #Returns a queryset of dictionaries
        context["contacto_data"] = contactos  # for the datalist
        context["contacto_data_json"] = json.dumps(list(contactos), cls=DjangoJSONEncoder)  # This is JSON string.
        return context

    def form_valid(self, form):
        # 1. Extract the values that came from the user in the form
        contacto = form.cleaned_data['contacto']
        email = form.cleaned_data['email_contacto']
        empresa = form.cleaned_data['cliente_empresa']

        # 2. Try to find an existing Cliente by `contacto`.
        # If not found, create a new one with the provided email and empresa.
        cliente, created = Cliente.objects.update_or_create(
                contacto=contacto,
                defaults={
                    'email_contacto': email,
                    'cliente_empresa': empresa
                }
            )

        # 3. Assign the Cliente to the Quote object before saving the Quote
        form.instance.cliente = cliente  # this sets the FK in the Quote model
        response = super().form_valid(form) #here we do the default steps to set the object and return the redirect

        self.send_quote_email(self.object)


        return redirect(f"{self.success_url}?email_sent=1")

    def send_quote_email(self, quote):
            subject = f"Cotización: {quote.nombre} - {quote.cliente.cliente_empresa}"
            recipient_email = quote.cliente.email_contacto
            user = quote.usuario

            # Prepare email content using a template
            message = render_to_string('quotes/email_quote.html', {
                'quote': quote,
                'user':user,
            })

            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email],
                cc=[user.email],
            )
            email.content_subtype = "html"  # Set to HTML

            # Attach PDF if exists
            if quote.pdf:
                email.attach_file(quote.pdf.path)  #Remember the quote.pdf is an object with attributes like .path and .url or .name

            email.send()


class QuoteDetailView(OwnerDetailView):
    model = Quote
    template_name = "quotes/quote_detail.html"

    def get(self, request, pk) :
        x = get_object_or_404(Quote, id=pk)
        context = { 'quote' : x }
        return render(request, self.template_name, context)


class QuoteUpdateView(OwnerUpdateView):

    #Option 1: You use a custom ModelForm
    # model = Quote
    # form_class = CreateForm #Here you are giving a custom ModelForm. This is when the create and update view share the same logic
    # template_name = 'quotes/quote_form.html'
    # success_url = reverse_lazy('quotes:quotes_all')

    #Option 2: You omit form_class and let Django autogenerate a form    
    model = Quote
    form_class = QuoteForm
    template_name = 'quotes/quote_form.html'
    success_url = reverse_lazy('quotes:quotes_all')


    def dispatch(self, request, *args, **kwargs):
        self.original_pdf = self.get_object().pdf #Retrieves the pdf from the Quote instance based on the pk from the URL
        return super().dispatch(request, *args, **kwargs)


    def get_initial(self):
        initial = super().get_initial()
        cliente = self.object.cliente
        if cliente:
            initial['contacto'] = cliente.contacto
            initial['email_contacto'] = cliente.email_contacto
            initial['cliente_empresa'] = cliente.cliente_empresa
        return initial
    
    def get_context_data(self, **kwargs): #This is for the method "get"
        context = super().get_context_data(**kwargs)
        contactos = Cliente.objects.all().values('contacto', 'email_contacto', 'cliente_empresa')
        context["contacto_data"] = contactos
        context["contacto_data_json"] = json.dumps(list(contactos), cls=DjangoJSONEncoder)
        return context


    def form_valid(self, form):
        contacto = form.cleaned_data['contacto']
        email = form.cleaned_data['email_contacto']
        empresa = form.cleaned_data['cliente_empresa']

        cliente, created = Cliente.objects.update_or_create(
            contacto=contacto,
            defaults={
                'email_contacto': email,
                'cliente_empresa': empresa
            }
        )

        form.instance.cliente = cliente
        response = super().form_valid(form)

        # ✅ Only send email if PDF changed
        if self.original_pdf != self.object.pdf:
            self.send_quote_email(self.object)
            return redirect(f"{self.success_url}?email_sent=1")
    
        return response


    def send_quote_email(self, quote):
            subject = f"Cotización: {quote.nombre} - {quote.cliente.cliente_empresa}"
            recipient_email = quote.cliente.email_contacto
            user = quote.usuario

            # Prepare email content using a template
            message = render_to_string('quotes/email_quote.html', {
                'quote': quote,
                'user':user,
            })

            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email],
                cc=[user.email],
            )
            email.content_subtype = "html"  # Set to HTML

            # Attach PDF if exists
            if quote.pdf:
                email.attach_file(quote.pdf.path)

            email.send()



    # def get(self, request, pk):
    #     quote = get_object_or_404(Quote, id=pk, usuario=self.request.user)
    #     form = CreateForm(instance=quote)
    #     ctx = {'form': form}
    #     return render(request, self.template_name, ctx)

    # def post(self, request, pk=None):
    #     quote = get_object_or_404(Quote, id=pk, usuario=self.request.user)
    #     form = CreateForm(request.POST, request.FILES or None, instance=quote)

    #     if not form.is_valid():
    #         ctx = {'form': form}
    #         return render(request, self.template_name, ctx)

    #     form.save()
    #     return redirect(self.success_url)


class QuoteDeleteView(OwnerDeleteView):
    model = Quote

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Quote

@require_POST
@login_required
def update_estado(request, pk):
    try:
        quote = Quote.objects.get(id=pk, usuario=request.user)
        new_estado = request.POST.get('estado')

        if new_estado not in dict(Quote.STATUS_CHOICES):
            return HttpResponseBadRequest("Estado inválido")

        quote.estado = new_estado
        quote.save()
        return JsonResponse({'success': True})
    except Quote.DoesNotExist:
        return JsonResponse({'error': 'Quote not found'}, status=404)


