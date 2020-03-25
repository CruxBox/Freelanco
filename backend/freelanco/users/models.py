from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up

LOCATION_CHOICES=[
    ('Hyd','Hyderabad'),
    ('MAS','Chennai')
]

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
    image=models.ImageField(upload_to='profile_image',blank=True,default="icon.png")

    #should add additional fields

    def __str__(self):
        return f"Customer-{self.user.username}"

    #creates customer profile for user who signup using google account
    @receiver(user_signed_up)
    def populate_profile(sociallogin,user,**kwargs):
        user.customer_profile=CustomerProfile()
        #user.customer_profile.image=user.socialaccount_set.filter(provider='google')[0].extra_data['picture']
        user.customer_profile.save()
class FreelancerProfile(models.Model):
    user=models.OneToOneField(to=CustomUser,on_delete=models.CASCADE,null=False,related_name="freelancer_profile")
    location=models.TextField(choices=LOCATION_CHOICES,max_length=None,default='Hyd')

   #add additional fields
    def __str__(self):
        return f"Freelancer-{self.user.username}"
