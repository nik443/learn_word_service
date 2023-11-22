from django.test import TestCase
from django.urls import reverse
from django.test import Client # Client - объект, имитирующий поведение пользователя
from django.test.utils import setup_test_environment


class HomePageTest(TestCase):

    def test_render(self):
        response = self.client.get(reverse('base_site:home'))
        self.assertEqual(response.status_code, 201) # проверка эквивалентности
        self.assertIn('Кстати, этот проект есть на GitGub', response.content.decode()) # проверка на вхождение 