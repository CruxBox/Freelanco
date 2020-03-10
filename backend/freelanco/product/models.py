from django.conf import settings
from django.db import models
from users.models import FreelancerProfile, CustomerProfile

class Item(models.Model):
	title = models.CharField(max_length=100)
	serviceCost = models.FloatField()
	discountedCost = models.FloatField()
	provider = models.ForeignKey(FreelancerProfile, on_delete = models.CASCADE)

	#Category left
	slug = models.SlugField()
	description = models.TextField()
	def __str__(self):
		return self.title

class OrderItem(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0)
	ordered = models.BooleanField(default=False)
	user = models.ForeignKey(CustomerProfile,
								on_delete=models.CASCADE)

	def __str__(self):
		return self.title


class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
								on_delete=models.CASCADE)

	items = models.ManyToManyField(OrderItem)
	# Cart creation time
	start_date = models.DateTimeField(auto_now_add=True)
	# Order time
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username
