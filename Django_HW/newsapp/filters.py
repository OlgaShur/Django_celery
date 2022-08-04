import django_filters
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, PostCategory, Category, Author
import django.forms


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='category',
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Author',
        empty_label='любой',
    )

    post_time_create = DateFilter(
        label='date',
        lookup_expr='gte',
        widget=django.forms.DateInput(
            attrs={
                'type': 'date'
            },
        )
    )

    class Meta:
        model = Post
        fields = {
            'name': ['icontains'],
            'description': ['icontains'],
            'type': ['exact'],
        }
