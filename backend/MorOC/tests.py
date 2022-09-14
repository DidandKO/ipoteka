from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BankOffersApiTestCase(APITestCase):
    def test_get(self):
        url = 'http://127.0.0.1:8000/api/bank_offers/'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
