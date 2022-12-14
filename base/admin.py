from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Topic, Articles, Messages
from .forms import CustomUserCreationForm
from django_summernote.admin import SummernoteModelAdmin
from mptt.admin import MPTTModelAdmin
# Register your models here.

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('email','username', 'is_staff', 'is_active', 'bio')
    
    fieldsets = (
        (None, {'fields': ('email','username', 'password', 'bio')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username' ,'password1', 'password2', 'is_staff', 'is_active', 'bio')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Topic)
admin.site.register(Articles,PostAdmin)
admin.site.register(Messages, MPTTModelAdmin)