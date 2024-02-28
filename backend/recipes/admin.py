from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from recipes.models import (
    FavoriteRecipe, Ingredient, RecipeIngredient, Recipe,
    RecipeInShoppingCart, Tag, TagRecipe
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit', 'usage_count']

    search_fields = ['name']

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).annotate(
            usage_count=Count('recipe')
        )

    def usage_count(self, obj):
        return obj.usage_count

    usage_count.short_description = _('Использований')
    usage_count.admin_order_field = 'usage_count'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug', 'usage_count']

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).annotate(
            usage_count=Count('recipe')
        )

    def usage_count(self, obj):
        return obj.usage_count

    usage_count.short_description = _('Использований')
    usage_count.admin_order_field = 'usage_count'


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1


class RecipeTagInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


class RecipeInShoppingCartInline(admin.TabularInline):
    model = RecipeInShoppingCart
    extra = 1


class FavoriteRecipeInline(admin.TabularInline):
    model = FavoriteRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'author',
        'cooking_time',
        'ingredient_count',
        'favorite_count',
        'shopping_cart_count',
    ]

    search_fields = [
        'name',
        'author__username',
        'author__first_name',
        'author__last_name',
        'author__email',
    ]

    inlines = [
        RecipeIngredientInline,
        RecipeTagInline,
        RecipeInShoppingCartInline,
        FavoriteRecipeInline,
    ]

    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs)
            .annotate(
                ingredient_count=Count('recipeingredient')
            )
            .annotate(
                shopping_cart_count=Count('recipeinshoppingcart')
            )
            .annotate(
                favorite_count=Count('favoriterecipe')
            )
        )

    def ingredient_count(self, obj):
        return obj.ingredient_count

    ingredient_count.short_description = _('Ингредиентов')
    ingredient_count.admin_order_field = 'ingredient_count'

    def shopping_cart_count(self, obj):
        return obj.shopping_cart_count

    shopping_cart_count.short_description = _('В корзине')
    shopping_cart_count.admin_order_field = 'shopping_cart_count'

    def favorite_count(self, obj):
        return obj.favorite_count

    favorite_count.short_description = _('В избранном')
    favorite_count.admin_order_field = 'favorite_count'
