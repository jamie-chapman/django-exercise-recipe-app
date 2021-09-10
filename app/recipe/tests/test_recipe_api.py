from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Recipe

RECIPE_URL = reverse('recipe:recipe-list')


def recipe_url(id):
    """Construct URL for a single recipe based on its ID"""
    return reverse('recipe:recipe-detail', args=[id])


def create_recipe(**params):
    """Helper function to create a user"""
    return Recipe.objects.create(**params)


class TestRecipeAPI(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload = {
            'name': 'Vegan Spaghetti Carbonara',
            'description': 'Spaghetti with vegan bacon, miso and nutritional yeast'
        }

        response = self.client.post(RECIPE_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload['name'], Recipe.objects.get(id=response.data['id']).name)

    def test_update_recipe(self):
        """Test updating a recipe"""
        self.recipe = Recipe.objects.create(
            name='Spaghetti Carbonara',
            description='Spaghetti with bacon, egg yolks and parmesan cheese'
        )

        payload = {
            'name': 'Vegan Spaghetti Carbonara',
            'description': 'Spaghetti with vegan bacon, miso and nutritional yeast'
        }

        response = self.client.patch(recipe_url(self.recipe.id), payload, format='json')
        self.recipe.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.recipe.name, payload['name'])

    def test_delete_recipe(self):
        """Test deleting a recipe"""
        self.recipe = Recipe.objects.create(
            name='Spaghetti Carbonara',
            description='Spaghetti with bacon, egg yolks and parmesan cheese'
        )

        response = self.client.delete(recipe_url(self.recipe.id), format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.all())
