from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from drug import models
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json

# Create your views here.
class APIView(generic.TemplateView):
    
    def get(self, request, *args, **kwargs ):
        result = '<h1>A wrong API request!</h1>'
        if request.method == 'GET':
            try:
                product_code = kwargs['product_code']
                prod = models.Product.objects.all().get(pk=product_code)
                reg = models.Registration.objects.get(pk=prod.reg_code_id)
                data = serializers.serialize('json', list([reg]) )
                return HttpResponse(data, content_type='application/json; charset=utf-8')
            except KeyError:
                pass
            except ObjectDoesNotExist:
                pass
            
        return HttpResponse(result);     
    