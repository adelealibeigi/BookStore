from .models import Category
from django.test import TestCase


class CategoryTests(TestCase):
    def test_create_product(self):
        category = Category.objects.create(
            title='dram',
            slug='dram-category'
            )

        self.assertEqual(category.title, 'dram')
        self.assertEqual(category.slug, 'dram-category')

