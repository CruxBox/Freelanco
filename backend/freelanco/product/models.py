from django.conf import settings
from django.db import models
from users.models import FreelancerProfile, CustomerProfile

class Item(models.Model):
	title = models.CharField(max_length=100)
	actual_cost = models.FloatField()
	discounted_cost = models.FloatField(default = -1)
	provider = models.ForeignKey(FreelancerProfile, on_delete = models.CASCADE)
	post_date = models.DateField(null=True,blank=True,auto_now_add=True)
	picture = models.ImageField(default = 'items/default.jpg', upload_to = 'items/uploads/% Y/% m/% d/')
	
	#Category left
	slug = models.SlugField()
	description = models.TextField()
	def __str__(self):
		return self.title

class OrderItem(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name = "order_item")
	quantity = models.IntegerField(default=0)
	ordered = models.BooleanField(default=False)
	user = models.ForeignKey(CustomerProfile,
								on_delete=models.CASCADE)

	def __str__(self):
		return self.item.title


class Order(models.Model):
	user = models.ForeignKey(CustomerProfile,
								on_delete=models.CASCADE)

	items = models.ManyToManyField(OrderItem)
	# Cart creation time
	start_date = models.DateTimeField(auto_now_add=True)
	# Order time
	ordered_date = models.DateTimeField(null=True, blank = True)
	ordered = models.BooleanField(default=False)

	def __str__(self):
		return self.user.user.username+" order"
