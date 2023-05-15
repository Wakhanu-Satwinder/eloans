from django.shortcuts import render
from django.urls import path
from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib.messages import constants as message_constants  

from django.contrib import auth
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm,ContactForm,LoginForm
from django.contrib.auth import authenticate,login, logout
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from .decorators import user_not_authenticated
#from . import helpers
from .models import Loans,Contact,CustomUser

from collections import OrderedDict

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import loansForm,ContactForm
from django.conf import settings

from django.urls import reverse_lazy
#from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage, get_connection

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q

from django.contrib.auth.tokens import default_token_generator

  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from .tokens import account_activation_token    
from django.core.mail import EmailMessage 



from .forms import SetPasswordForm
from django.contrib.auth import get_user_model


#import smtplib # import smtp library in your Python script to fix the error.
# Create your views here.
'''def home(request):
    return render(request, 'home.html', {})'''
@login_required(login_url='login')
def home(request):
    return render(request,'pages/home.html',{})

#...
@user_not_authenticated
def register(request):
    if request.method == 'POST':
        f = UserRegisterForm(request.POST)
        if f.is_valid():

        	#ADDED
           user = f.save(commit=False)  
           user.is_active = False 
           user.save()
           #added
           # to get the domain of the current site  
           current_site = get_current_site(request)  
           mail_subject = 'Activation link has been sent to your email id'  
           message = render_to_string('pages/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            
           to_email = f.cleaned_data.get('email')  
           email = EmailMessage(mail_subject, message, to=[to_email])  
           email.send()  
           return HttpResponse('Please confirm your email address to complete the registration') 

            #OLD 
        '''f.save()'''
            
            #original

        '''messages.success(request, 'Account created successfully')
        return redirect('login')'''


    else:
        f = UserRegisterForm()
 
    return render(request, 'pages/register.html', {'form': f})


#@login_required(login_url='login')
def index(request):
    return render(request,'pages/index.html',{})

    
def logout(request):
    auth.logout(request)
    try:
        del request.session['username']
        request.session.flush()
    except:
        messages.info(request,"You Logged out Successfully")
        return render(request,"pages/logout.html",{})

'''@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")'''

def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                #login(request,user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="pages/login.html", context={"login_form":form})




@login_required(login_url='login')
def profile(request):
    #loans=Loans.objects.all()
      loans=Loans.objects.filter(customuser=request.user)
      return render(request,'pages/profile.html',{'loans':loans})


@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            contact = form.save(commit=False)
            contact.customuser = request.user
            contact.save()
            messages.success(request, 'Review submitted successfully')
            return render(request,'pages/review_success.html',{'form': form}) 
    else:
        form = ContactForm()
    return render(request,'pages/contact.html',context={'form': form})


@login_required(login_url='login')
def loans(request):
   # loans=Loans.objects.get(pk.pk)
    if request.method == 'POST':
        f = loansForm(request.POST)
        if f.is_valid():
           loans = f.save(commit=False)
           loans.customuser = request.user

           loans.save()
           messages.success(request, 'Loan Applied pending approval')
           return redirect('home')
    else:
        #messages.error(request,"Check your details.")
        f = loansForm()
 
    return render(request, 'pages/loans.html', {'form': f})






def send_email(request):  
   if request.method == "POST": 
       with get_connection(  
           host=settings.EMAIL_HOST, 
     port=settings.EMAIL_PORT,  
     username=settings.EMAIL_HOST_USER, 
     password=settings.EMAIL_HOST_PASSWORD, 
     use_tls=settings.EMAIL_USE_TLS  
       ) as connection:  
           subject = request.POST.get("subject")  
           email_from = settings.EMAIL_HOST_USER  
           recipient_list = [request.POST.get("email"), ]  
           message = request.POST.get("message")  
           EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()  
 
   return render(request, 'home.html')



#@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password/password_reset_confirm.html', {'form': form})


@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = CustomUser.objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("password/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                       Password reset sent|
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('home')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(request=request,template_name="password/password_reset.html", context={"form": form})



@user_not_authenticated
def passwordResetConfirm(request, uidb64, token):
    customuser = request.user
    if request.method == 'POST':
        form = SetPasswordForm(customuser,request.POST)
        if form.is_valid():
           customuser = CustomUser.objects.get(pk=uid)
           form.save()
           messages.success(request, "Your password has been changed")
        return redirect('login')

    else:
        for error in list(form.errors.values()):
          messages.error(request, error)

    form = SetPasswordForm(customuser)
    return render(request, 'password/password_reset_confirm.html', {'form': form})
    #return redirect("home")




def activateEmail(request, user, to_email):
    messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
        received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = CustomUser.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')

        messages.success(request,f'Thank you for your email confirmation. Now you can login your account.')
        return render(request,'pages/log.html',{})  
    else:  
        return HttpResponse('Activation link is invalid!')  