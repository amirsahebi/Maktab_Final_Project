import django_filters

from post.models import Post
from shop.models import Product, Store


class StoreListFilter(django_filters.FilterSet):
    # creator_isnull = django_filters.BoleanFilter(field_name='creator', lookup_expr='isnull')
    # filter_fields = {
    #     'likes': ['gte', 'lte']
    # }

    class Meta:
        model = Store
        fields = ['type']


class StoreProductListFilter(django_filters.FilterSet):
    # creator_isnull = django_filters.BoleanFilter(field_name='creator', lookup_expr='isnull')
    
    class Meta:
        model = Product
        fields = {
            'cost': ['lte', 'gte'],
            'tag':['exact','lte'],
            'availablity':['exact','lte'],
        }