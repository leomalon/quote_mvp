from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerQuerySetMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(usuario=self.request.user)

class OwnerListView(LoginRequiredMixin,ListView):

    def get_queryset(self):
        return self.model.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')

class OwnerCreateView(LoginRequiredMixin, CreateView):

    # We override "form_valid" to save the attribute of usuario.
    def form_valid(self, form):
        self.object = form.save(commit=False) #The "object" attribute is to refer to the instance of the model just created
        self.object.usuario = self.request.user
        self.object.save()
        return super().form_valid(form) #Since we are overriding we still want Django to do the other default stuff (like assign self.object and redirect using success_url)

class OwnerDetailView(OwnerQuerySetMixin,LoginRequiredMixin,DetailView):
    """
    Sub-class the DetailView to pass the request to the form.
    """

class OwnerUpdateView(OwnerQuerySetMixin,LoginRequiredMixin,UpdateView):

    """
    Sub-class the UpdateView
    """


class OwnerDeleteView(OwnerQuerySetMixin,LoginRequiredMixin,DeleteView):

    """
    Sub-class the DeleteView
    """
