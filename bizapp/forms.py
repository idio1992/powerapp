from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile,ShopCart, PaidOrder

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone', 'address', 'city', 'state', 'img')

class ShopCartForm(forms.ModelForm):
    class Meta:
        model = ShopCart
        fields = ('quantity',)  

class PaidOrderForm(forms.ModelForm):
    class Meta:
        model = PaidOrder
        fields = ('first_name', 'last_name', 'phone', 'address', 'city', 'state')              