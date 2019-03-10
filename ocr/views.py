from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from ocr import forms

# Create your views here.
class GetView(generic.TemplateView):
  template_name = 'ocr/get.html'
  def get(self, request, *args, **kwargs ):
      return render(request, self.template_name, {})
        
  def post(self, request, *args, **kwargs ):
      return render(request, self.template_name, {})