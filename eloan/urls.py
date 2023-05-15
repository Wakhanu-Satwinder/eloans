from django.urls import path,include

from .views import home,register,login,logout,loans,profile,index,contact,password_change,password_reset_request,activate 
from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

#ADDED CODE
#from users import views as user_views
#app_name = "eloan"


urlpatterns = [
    path('home/', views.home, name='home'),
    path('loans/', views.loans, name='loans'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('index/', views.index, name='index'),
    path('logout', auth_views.LogoutView.as_view(template_name='pages/logout.html'), name='logout'),
    path('login', auth_views.LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('contact/', views.contact, name='contact'),

    path('password_change', views.password_change, name="password_change"),


    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        activate, name='activate'),  

   # path("password_reset", views.password_reset_request, name="password_reset"),

   # path('password_reset/', ResetPasswordView.as_view(template_name='pages/password_reset.html'), name='password_reset'),
    
    #path('login/', views.login, name='login'),
    #path('logout/', authentication.views.logout_user, name='logout'),
]

# Only add this when we are in debug mode.
'''if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)'''