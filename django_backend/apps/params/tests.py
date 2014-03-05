"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import unittest
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import authenticate, login
from apps.params.models import Locality

class SimpleTest(TestCase):
	def setUp(self):
		
		Locality.objects.create(name="lion", location="roar")
		Locality.objects.create(name="cat", location="meow")

	def test_basic_addition(self):
		"""
		Tests that 1 + 1 always equals 2.
		"""
		lion = Locality.objects.get(name="lion")
		self.assertEqual(lion.name,"lion")

		response = self.client.get('/params/locality/index/')
		self.assertEqual(response.status_code, 200)

		self.assertEqual(1 + 1, 2)

		#user = self.client.login(self.client, password="12345")
		#self.assertTrue(user) #assertIsNotNone assertRaises(exception)


