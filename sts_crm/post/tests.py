from django.test import TestCase
from .models import Istoriya


class AnimalTestCase(TestCase):
    def setUp(self):
        Istoriya.objects.create(title="lion", text="roar")
        Istoriya.objects.create(ttile="cat", test="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Istoriya.objects.get(name="lion")
        cat = Istoriya.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
