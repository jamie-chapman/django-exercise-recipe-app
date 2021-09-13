from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Recipe

RECIPE_URL = reverse('recipe:recipe-list')


def recipe_url(id):
    """Construct URL for a single recipe based on its ID"""
    return reverse('recipe:recipe-detail', args=[id])


def create_sample_recipe(**params):
    """Helper function to create a user"""
    return Recipe.objects.create(**params)


class RecipeAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload = {
            'name': 'Vegan Roast Dinner',
            'description': 'Roasted potatoes and mushroom wellington'
                           ' with vegetables and gravy.',
            'ingredients': [
                {'name': 'Potatoes'},
                {'name': 'Carrots'},
                {'name': 'Brussels Sprouts'},
                {'name': 'Pastry'},
                {'name': 'Chestnut Mushrooms'}
            ]
        }

        response = self.client.post(RECIPE_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            payload['name'],
            Recipe.objects.get(id=response.data['id']).name
        )

    def test_get_recipe(self):
        """Test updating a recipe"""
        create_sample_recipe(
            name='Roast Dinner',
            description='Roasted potatoes and chicken'
                        ' with vegetables and gravy.'
        )

        response = self.client.get(RECIPE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_recipe(self):
        """Test updating a recipe"""
        self.recipe = create_sample_recipe(
            name='Roast Dinner',
            description='Roasted potatoes and chicken'
                        ' with vegetables and gravy.'
        )

        payload = {
            'name': 'Vegan Roast Dinner',
            'description': 'Roasted potatoes and mushroom wellington'
                           ' with vegetables and gravy.'
        }

        response = self.client.patch(
            recipe_url(self.recipe.id),
            payload, format='json'
        )

        self.recipe.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.recipe.name, response.data['name'])
        self.assertEqual(self.recipe.description, response.data['description'])

    def test_delete_recipe(self):
        """Test deleting a recipe"""
        self.recipe = create_sample_recipe(
            name='Carrot Cake',
            description='Sponge cake with hella carrots.'
        )

        response = self.client.delete(
            recipe_url(self.recipe.id),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.all())

    def test_create_recipe_with_ingredients(self):
        """Test creating a recipe including ingredients"""
        payload = {
            'name': 'Vegan Roast Dinner',
            'description': 'Roasted potatoes and mushroom wellington'
                           ' with vegetables and gravy.',
            'ingredients': [
                {'name': 'carrots'},
                {'name': 'potatoes'},
                {'name': 'mushrooms'},
            ]
        }

        response = self.client.post(RECIPE_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            payload['name'],
            Recipe.objects.get(id=response.data['id']).name
        )
        self.assertEquals(
            len(response.data['ingredients']),
            len(payload['ingredients'])
        )
