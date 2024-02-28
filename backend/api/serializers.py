import base64
import logging
import uuid

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser import serializers as djoser_serializers
from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeInShoppingCart,
    Subscription,
    Tag,
    TagRecipe,
)
from rest_framework import serializers

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            file_name = str(uuid.uuid4())
            file_extension = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=file_name + '.' + file_extension
            )

        return super().to_internal_value(data)


class UserCreateSerializer(djoser_serializers.UserCreateSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        ]


class UserSerializer(djoser_serializers.UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if not user or user.is_anonymous:
            return False
        queryset = Subscription.objects.all()
        return queryset.filter(user=user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'color',
            'slug',
        ]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'measurement_unit',
        ]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount',
        ]


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set',
        many=True,
        read_only=True,
    )

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        ]

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        if not user or user.is_anonymous:
            return False
        queryset = RecipeInShoppingCart.objects.all()
        return queryset.filter(recipe=obj, user=user).exists()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        if not user or user.is_anonymous:
            return False
        queryset = FavoriteRecipe.objects.all()
        return queryset.filter(recipe=obj, user=user).exists()


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = RecipeIngredient
        fields = [
            'id',
            'amount',
        ]


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        ]

    def create_related_ingredients(self, recipe, ingredients_data):
        recipe_ingredients = []
        for ingredient_data in ingredients_data:
            recipe_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient_data['ingredient']['id'],
                amount=ingredient_data['amount'],
            )
            recipe_ingredients.append(recipe_ingredient)
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def create_related_tags(self, recipe, tags_data):
        recipe_tags = []
        for tag_data in tags_data:
            recipe_tag = TagRecipe(
                recipe=recipe,
                tag=tag_data,
            )
            recipe_tags.append(recipe_tag)
        TagRecipe.objects.bulk_create(recipe_tags)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        instance = super().create(validated_data)

        self.create_related_ingredients(instance, ingredients_data)
        self.create_related_tags(instance, tags_data)

        return instance

    def update(self, instance, validated_data):
        RecipeIngredient.objects.filter(recipe=instance).delete()
        TagRecipe.objects.filter(recipe=instance).delete()

        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        instance = super().update(instance, validated_data)

        self.create_related_ingredients(instance, ingredients_data)
        self.create_related_tags(instance, tags_data)

        return instance

    def to_representation(self, instance):
        return RecipeSerializer(
            instance, context={'request': self.context.get('request')}
        ).data


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]


class UserWithRecipesSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if not user or user.is_anonymous:
            return False
        queryset = Subscription.objects.all()
        return queryset.filter(user=user, author=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj)
        if limit:
            queryset = queryset[: int(limit)]
        return ShortRecipeSerializer(queryset, many=True).data

    # noinspection PyMethodMayBeStatic
    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
