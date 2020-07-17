from django import forms 
from .models import Item

class ItemEditForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=('title', 'category', 'actual_cost', 'discounted_cost','post_date','picture','slug','description')