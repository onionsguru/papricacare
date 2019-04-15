from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from hospital import models
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json

# Create your views here.
class APIView(generic.TemplateView):
    
    def get(self, request, *args, **kwargs ):
        result = '<h1>A wrong API request!</h1>'
        if request.method == 'GET':
            try:
                table_name = kwargs['table']
                col_name = kwargs['col']
                table = getattr(models, table_name)
                data = list(table.objects.values_list(col_name, flat=True))
                # print(data)
                return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
            except KeyError:
                pass
            except ObjectDoesNotExist:
                pass
            
        return HttpResponse(result);