from django_filters import rest_framework as filters
from .models import Kurs
class ProductFilter(filters.FilterSet):
    class Meta:
        model = Kurs
        fields = {
            'category': ['exact'],
            'viloyatlar': ['exact']
        }