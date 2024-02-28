from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters
from recipes.models import Recipe, Tag
from rest_framework.filters import SearchFilter

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_('Автор'),
    )
    is_favorited = filters.BooleanFilter(
        label=_('В избранном'), field_name='is_favorited', method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        label=_('В корзине'),
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart',
    )
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        label=_('Теги'),
        field_name='tags__slug',
        to_field_name='slug',
    )

    class Meta:
        model = Recipe
        fields = [
            'author',
            'is_favorited',
            'is_in_shopping_cart',
            'tags',
        ]

    def filter_is_favorited(self, queryset, field_name, value):
        user = self.request.user
        if not user or user.is_anonymous:
            return queryset
        if value == True:
            return queryset.filter(favoriterecipe__user=user)
        if value == False:
            return queryset.excluse(favoriterecipe__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, field_name, value):
        user = self.request.user
        if not user or user.is_anonymous:
            return queryset
        if value == True:
            return queryset.filter(recipeinshoppingcart__user=user)
        if value == False:
            return queryset.excluse(recipeinshoppingcart__user=user)
        return queryset


class IngredientFilter(SearchFilter):
    search_param = 'name'
