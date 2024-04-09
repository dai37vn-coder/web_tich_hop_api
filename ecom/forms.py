from django import forms
from django.contrib.auth.models import User
from . import models
import json
import requests


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile','profile_pic']

class ProductForm(forms.ModelForm):
    class Meta:
        model=models.Product
        fields=['name','price','description','product_image']

#address of shipment
class AddressForm(forms.Form):
    Email = forms.EmailField()
    Mobile= forms.IntegerField()
    Address = forms.CharField(max_length=500)
    

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['name','feedback']

#for updating status of order
class OrderForm(forms.ModelForm):
    class Meta:
        model=models.Orders
        fields=['status']

#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'custom-name-class'}))
    Email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'custom-email-class'}))
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'custom-message-class', 'rows': 3, 'cols': 30}))
    

#for post
class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'content','author', 'published_at', 'post_image']
    
