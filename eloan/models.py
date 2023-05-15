from django.db import models
from django.conf import settings
# Create your models here.
from django.db.models.fields import EmailField,CharField,TextField
from django.contrib.auth.models import User


#from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
#from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext as _

#from .managers import CustomUserManager
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from .managers import CustomUserManager
#from django.contrib.contenttypes.fields import GenericForeignKey
from django.core import validators


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    
    email = models.EmailField(_('email address'), max_length=254, unique=True, validators=[validators.EmailValidator(message="Invalid Email")])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    username = models.CharField(_('Username'), max_length=30, blank=True)
    phone_no = models.IntegerField(_('Phone Number'),blank=True,default=False)
    id_number = models.IntegerField(_('ID Number'), blank=True ,default=False)
    county = models.CharField(_('County'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


    def __str__(self):
      
           return f"{self.id} {self.username}"








class Loans(models.Model):
    """docstring for loansForm"""
   
    
    #CustomUser=models.ForeignKey(CustomUser,on_delete=models.CASCADE,default="")
   #customuser=models.oCustomUser,on_delete=models.CASCADE)
    loans_id=models.AutoField(primary_key=True)
    customuser=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    first_name=models.CharField(_('first name'),max_length=10)
    last_name=models.CharField(_('last name'),max_length=10)
    phone_no=models.CharField(_('phone number'),max_length=10)
    id_number=models.CharField(_('id number'),unique=True,max_length=10)
    county=models.CharField(_('county '),max_length=10)
    loan_amt=models.CharField(_('loan_amt'),max_length=5)
    applied_on=models.DateTimeField(auto_now_add=True)
    #object_id = models.PositiveIntegerField()
    #content_object = GenericForeignKey('content_type', 'object_id')
    #customuser=models.ForeignKey('CustomUser',on_delete=models.CASCADE)

    #customuser=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    
'''class Meta:
        db_table = u'loans'
        list_display=('first_name','last_name','phone_no','id_number','county','loan_amt')'''

def __str__(self):
        return f"{self.customuser_id} {self.first_name} {self.last_name}{self.phone_no} {self.loan_amt}"

'''def __init__(self, arg):
          super(loansForm, self).__init__()
          self.arg = arg'''




class Contact(models.Model):
    """docstring for Contact"""
    customuser=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    username=models.CharField(max_length=100)
    email=models.EmailField('email adress',unique=True)
    subject=models.CharField( max_length=255)
    review=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    '''class Meta:    
       #model=Contact
       fields=['username','email','subject','review']

       def __init__(self, arg):
           super(Contact, self).__init__()
           self.arg = arg'''

    def __str__(self):
      
           return f"{self.username} {self.email} {self.subject} {self.review}"



