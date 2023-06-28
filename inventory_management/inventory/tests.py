from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import InventoryItem, Category

# class BasicTests(TestCase):
# 	def test_1(self):
# 		self.assertTrue(1==1)
# 		# self.assertTrue(1==2)

	# def test_2(self):
	# 	try:
	# 		# print("Hello!")
	# 		raise Exception('Failure in test_2')
	# 	except Exception as e:
	# 		self.fail(e)

class TestModels(TestCase):
	def setUp(self):
		"""
		Set up before each test
		"""
		self.user = User.objects.create_user(username='testuser', password='password')
		self.category = Category.objects.create(name='Test Category')

	def test_model_InventoryItem(self):
		# 1. set up code
		# 2. logic to test
		# 3. assertions

		inventory_item = InventoryItem.objects.create(
			name='Test Item',
			quantity=10,
			user=self.user,
			category=self.category
		)

		self.assertEquals(str(inventory_item), 'Test Item')
		self.assertTrue(isinstance(inventory_item, InventoryItem))

class TestViews(TestCase):
	def setUp(self):
		self.client = Client()

		self.user = User.objects.create_user(username='testuser', password='password')
		self.client.login(username='testuser', password='password')

		self.category = Category.objects.create(name='Test Category')
		
		self.inventory_item = InventoryItem.objects.create(
			name='Test Item',
			quantity=10,
			user=self.user,
			category=self.category
		)

		# urls
		self.index_url = reverse('index')
		self.dashboard_url = reverse('dashboard')
		self.add_item_url = reverse('add-item')
		self.edit_item_url = reverse('edit-item', args=[self.inventory_item.id])
		self.delete_item_url = reverse('delete-item', args=[self.inventory_item.id])

	def test_index_GET(self):
		# mock the response
		response = self.client.get(self.index_url)

		# write assertions
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'inventory/index.html')

	def test_dashboard_GET(self):
		response = self.client.get(self.dashboard_url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'inventory/dashboard.html')

	def test_dashboard_GET_not_logged_in(self):
		self.client.logout()

		response = self.client.get(self.dashboard_url)

		self.assertEquals(response.status_code, 302)

	def test_add_item_POST(self):
		response = self.client.post(self.add_item_url, {
			'name': 'Test Item 2',
			'quantity': 15,
			'user': self.user.id,
			'category': self.category.id
		})

		self.assertEquals(response.status_code, 302)
		self.assertEquals(InventoryItem.objects.count(), 2)
		self.assertEquals(InventoryItem.objects.last().name, 'Test Item 2')

	def test_item_POST_no_data(self):
		response = self.client.post(self.add_item_url)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(InventoryItem.objects.count(), 1)

	def test_edit_item_POST(self):
		response = self.client.post(self.edit_item_url, {
			'name': 'Updated Test Item',
			'quantity': 10,
			'user': self.user.id,
			'category': self.category.id
		})

		self.inventory_item.refresh_from_db()

		self.assertEquals(response.status_code, 302)
		self.assertEquals(InventoryItem.objects.first().name, 'Updated Test Item')
		self.assertEquals(InventoryItem.objects.count(), 1)

	def test_delete_item_DELETE(self):
		response = self.client.delete(self.delete_item_url)

		self.assertEquals(response.status_code, 302)
		self.assertEquals(InventoryItem.objects.count(), 0)