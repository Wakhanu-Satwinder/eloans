from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm
#from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from  django.forms import ModelForm
from .models import Contact,Loans,CustomUser
#from .models import User


'''from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField'''

from .models import CustomUser

from django.contrib.auth.forms import SetPasswordForm,PasswordResetForm



class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)
#Original
'''class RegisterForm(UserCreationForm):
	email=forms.EmailField()
	password1=forms.CharField(max_length=10)
	password2=forms.CharField(max_length=10)
	class meta:
		model=User
		fields=["username","email","password1","password2"]'''

class UserRegisterForm(UserCreationForm):
    username= forms.CharField(min_length=4,max_length = 20)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_no = forms.CharField(min_length=10 ,max_length =15)
    first_name = forms.CharField(min_length=4, max_length = 20)
    last_name = forms.CharField(min_length=4,max_length = 20)
    id_number= forms.CharField(min_length=6,max_length =12)
    county = forms.CharField(max_length = 20)
    password1=forms.CharField(max_length=10,label='Password', widget=forms.PasswordInput)
    password2=forms.CharField(max_length=10,label='Confirm Password', widget=forms.PasswordInput)
    class Meta:
        #model = User
        model = CustomUser
        fields = ['username', 'email', 'phone_no','first_name','last_name','id_number','county', 'password1', 'password2']


'''class CustomUserCreationForm(forms.Form): 
    
    username = forms.CharField(label='Username', min_length=4, max_length=15)  
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)



    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email
 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
 
        return password2
 
    def save(self, commit=True):
        user = User.objects.create_user(
            
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
'''


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', min_length=4, max_length=16)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
	
    class Meta:
        #model = User
        model = CustomUser
        fields = ['username', 'password']
		


class loansForm(forms.ModelForm):
    """docstring for loans"""
    
    first_name=forms.CharField(max_length=10,label='Guaranters first name')
    last_name=forms.CharField(max_length=10,label='Guaranters last name')
    phone_no=forms.CharField(max_length=10,label='Guaranters Phone no')
    id_number=forms.CharField(max_length=10,label='Guaranters ID')
    county=forms.CharField(max_length=10,label='Guaranters county')
    loan_amt=forms.CharField(max_length=5,label='Enter Loan Amt')

    class Meta:
        model = Loans
        fields = ['first_name', 'last_name', 'phone_no','id_number','county','loan_amt']
         
        def __init__(self, arg):
            super(loansForm, self).__init__()
            self.arg = arg
        def __str__(self):
      
            return f"{self.first_name} {self.last_name} {self.phone_no} {self.id_number} {self.county} {self.loan_amt}"
        


class ContactForm(forms.ModelForm):
    #customuser=forms.CharField()
    username=forms.CharField(max_length=100, label="Enter Your Name")
    email=forms.EmailField( label=" Enter your Email")
    subject = forms.CharField(max_length=100)
    review= forms.CharField(widget=forms.Textarea(attrs={'rows':3,'cols':30}),required=True)

    class Meta:
        model = Contact
        fields = ['username', 'email', 'subject','review']
        #exclude=['customuser']

        def __init__(self, arg):
            super(ContactForm, self).__init__()
            self.arg = arg
        def __str__(self):
      
            return f"{self.username} {self.email} {self.subject} {self.review}"



...
class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = CustomUser
        fields = ['new_password1', 'new_password2']


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())