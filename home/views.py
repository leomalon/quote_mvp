from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
    

class HomeView(LoginRequiredMixin,View): 
    def get(self, request):
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >=0 #checks if the request is coming from a local environment
        context = { #this just creates the context of all the installed Django apps
            'installed' : settings.INSTALLED_APPS,
            'islocal':islocal,
            'app':settings.APP_NAME
        }
        return render(request,'home/main.html',context)