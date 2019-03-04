from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

class HomeView(generic.TemplateView):
    template_name = 'home.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {}) 
        '''
        if request.user.is_authenticated == True:
            return HttpResponseRedirect(reverse('chat:index'))
        else:
            return render(request, self.template_name, {}) 
        '''