from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

LOCATION_CHOICES=[
    ('Hyd','Hyderabad'),
    ('MAS','Chennai')
]
    
# Create your models here.
class CustomUser(AbstractUser):
    """
    Extended from Abstract User
    List of inherited fields: first_name, last_name, email, username, password
    """
    is_freelancer=models.BooleanField(default=False)

class CustomerProfile(models.Model):
    user=models.OneToOneField(to=CustomUser,on_delete=models.CASCADE,null=False,related_name="customer_profile")
    location=models.TextField(choices=LOCATION_CHOICES,max_length=None,default='Hyd')
    #should add additional fields

    def __str__(self):
        return f"Customer-{self.user.username}"

class FreelancerProfile(models.Model):
    user=models.OneToOneField(to=CustomUser,on_delete=models.CASCADE,null=False,related_name="freelancer_profile")
    location=models.TextField(choices=LOCATION_CHOICES,max_length=None,default='Hyd')

   #add additional fields

    def __str__(self):
        return f"Freelancer-{self.user.username}"

"""
@receiver(post_save, sender=CustomUser)
def create_or_update_user(sender, instance,created,**kwargs):
    if created:
        print("Damne")
        if instance.is_freelancer:
            profile=FreelancerProfile.objects.create(user=instance)
        else:
            profile=CustomerProfile.objects.create(user=instance)
"""