from rest_framework import serializers, viewsets, generics
import drug

# Serializers define the API representation.
class ProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = drug.models.Product
        fields = ('__all__')

class RegiSerializer(serializers.ModelSerializer):
    class Meta:
        model = drug.models.Registration
        fields = ('__all__')

class IngreSerializer(serializers.ModelSerializer):
    class Meta:
        model = drug.models.Ingredient
        fields = ('__all__')

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = drug.models.IngreForm
        fields = ('__all__')
        
class DescSerializer(serializers.ModelSerializer):
    class Meta:
        model = drug.models.IngreDesc
        fields = ('__all__')
        
class DrugNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = drug.models.Registration
        fields = ('__all__')
        
# ViewSets define the view behavior.
class ProdViewSet(viewsets.ModelViewSet):
    queryset = drug.models.Product.objects.all()
    serializer_class = ProdSerializer
    
class RegiViewSet(viewsets.ModelViewSet):
    queryset = drug.models.Registration.objects.all()
    serializer_class = RegiSerializer
    
class IngreViewSet(viewsets.ModelViewSet):
    queryset = drug.models.Ingredient.objects.all()
    serializer_class = IngreSerializer
    
class FormViewSet(viewsets.ModelViewSet):
    queryset = drug.models.IngreForm.objects.all()
    serializer_class = FormSerializer
    
class DescViewSet(viewsets.ModelViewSet):
    queryset = drug.models.IngreDesc.objects.all()
    serializer_class = DescSerializer
    
class DrugNameViewSet(generics.ListAPIView):
    serializer_class = DrugNameSerializer
    
    def get_queryset(self):
        return drug.models.Registration.objects.filter(drug_name__contains=self.kwargs['name'])