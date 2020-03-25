from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

LOCATION_CHOICES=[
    ('Hyd','Hyderabad'),
    ('MAS','Chennai')
]
    
# Create your models here.

class Address(models.Model):
    address1 = models.CharField("Address line 1", max_length=1024)
    address2 = models.CharField("Address line 2", max_length=1024, blank=True, null=True)
    pin_code = models.CharField("PIN", max_length=6)
    city = models.CharField("City", max_length=20)
    state=models.CharField("State",max_length=20)
    
class CustomUser(AbstractUser):
    """
    Extended from Abstract User
    List of inherited fields: first_name, last_name, email, username, password
    """
    is_freelancer=models.BooleanField(default=False)

class CustomerProfile(models.Model):
    user=models.OneToOneField(to=CustomUser,on_delete=models.CASCADE,null=False,related_name="customer_profile")
    location=models.TextField(choices=LOCATION_CHOICES,max_length=None,default='Hyd')
    address=models.OneToOneField(to=Address,on_delete=models.CASCADE,null=True,related_name="customer_address")
    image=models.ImageField(upload_to='profile_image',blank=True)

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