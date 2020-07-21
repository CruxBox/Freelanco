from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up
from django.contrib.contenttypes.fields import GenericForeignKey

LOCATION_CHOICES=(
    ('Hyd','Hyderabad'),
    ('MAS','Chennai'),
    ('Bom','Mumbai')
)


class CustomUser(AbstractUser):
    """
    Extended from Abstract User
    List of inherited fields: first_name, last_name, email, username, password
    """
    is_freelancer=models.BooleanField(default=False)

class CustomerProfile(models.Model):

    """
    Stores Details of Customer, related to :model:`users.CustomUser`.
    """

    user=models.OneToOneField(to=CustomUser,on_delete=models.CASCADE,null=False,related_name="customer_profile")
    location=models.TextField(choices=LOCATION_CHOICES,max_length=None,default='Hyd')
    #address=models.OneToOneField(to=Address,on_delete=models.CASCADE,null=True,related_name="customer_address")
    image=models.ImageField(upload_to='profile_image',blank=True,default="icon.png")
    phone=models.CharField(max_length=15,null=True,blank=True)

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
    """
    Stores Details of Freelancer, related to :model:`users.CustomUser`.
    """
    user=models.OneToOneField(to=CustomUser,on_delete=models.CASCADE,null=False,related_name="freelancer_profile")
    location=models.TextField(choices=LOCATION_CHOICES,max_length=None,default='Hyd')
    phone=models.CharField(max_length=15,null=True,blank=True)

   #add additional fields
    def __str__(self):
        return f"Freelancer-{self.user.username}"

class Address(models.Model):
    """
    Stores Details of the address of a Customer or a Freelancer, related to :model:`users.CustomerProfile`
    and :model:`users.CustomerProfile`.
    """
    name=models.CharField("Name", max_length=100,blank=True,null=True)
    address1 = models.CharField("Address line 1", max_length=1024)
    address2 = models.CharField("Address line 2", max_length=1024, blank=True, null=True)
    pin_code = models.CharField("PIN", max_length=6, blank=True, null=True)
    city = models.CharField("City", max_length=20, blank=True, null=True,choices=LOCATION_CHOICES)
    state=models.CharField("State",max_length=20, blank=True, null=True)
    customer=models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,related_name='addresses',null=True,blank=True)
    freelancer=models.ForeignKey(FreelancerProfile,on_delete=models.CASCADE,related_name='addresses',null=True,blank=True)

    class Meta:
       unique_together = ("name", "customer")