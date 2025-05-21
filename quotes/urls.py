from django.urls import path, reverse_lazy
from . import views


app_name='quotes'
urlpatterns = [

    path('', views.QuoteListView.as_view(),name = "quotes_all"),
    path('quote/<int:pk>', views.QuoteDetailView.as_view(), name='quote_detalle'),
    path('quote/create',
        views.QuoteCreateView.as_view(success_url=reverse_lazy('quotes:quotes_all')), name='quote_create'),
    path('quote/<int:pk>/update',
        views.QuoteUpdateView.as_view(success_url=reverse_lazy('quotes:quotes_all')), name='quote_update'),
    path('<int:pk>/update_estado',views.update_estado, name='update_estado'),
    path('quote/<int:pk>/delete',
        views.QuoteDeleteView.as_view(success_url=reverse_lazy('quotes:quotes_all')), name='quote_delete')

]