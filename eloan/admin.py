from django.contrib import admin
from .models import Contact,Loans,User

#from .forms import CustomUserCreationForm, CustomUserChangeForm

from django.contrib.auth import get_user_model
#from .models import UserShippingAddressGroup
#from .forms import UserAdminChangeForm, UserAdminCreationForm
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.utils.translation import ugettext_lazy as _



from django.contrib.auth import get_user_model

User = get_user_model()
class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('username','email', 'first_name', 'last_name','phone_no','id_number','county', 'is_staff','is_active','date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)




# Register your models here.
User = get_user_model()
class ContactAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'subject', 'review','created_on')
    list_filter = ['created_on']
    search_fields = ['username']

class LoansAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_no', 'id_number','county','loan_amt','applied_on')
    list_filter = ['loan_amt']
    search_fields = ['first_name', 'last_name', 'phone_no', 'id_number','county','loan_amt','applied_on']
   
#admin.site.register(User)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Loans,LoansAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.site_url = "/eloans/home"

#admin.site.register(User,UserInAdmin)
#admin.site.register(CustomUser, CustomUserAdmin)

