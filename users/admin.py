from django.contrib import admin
from .models import UserAlert, UserData, models
from django.forms import CheckboxSelectMultiple

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'provider', 'phone_no')
    search_fields = ('email', 'phone_no')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserAlertAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'coin_name', 'default_alert', 'last_send_email')
    search_fields = ('user_email', 'coin_name')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(UserData, UserAdmin)
admin.site.register(UserAlert, UserAlertAdmin)