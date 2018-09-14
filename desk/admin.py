from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Day, Sector, Row, Seat, City, Cache

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('full_name', 'email', 'admin')
    list_filter = ('admin', 'staff', 'active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'full_name')}),
        ('Stats', {'fields': ('gain', 'sold_normal', 'sold_share', 'sold_vacant', 'batch')}),
        ('Tickets', {'fields': (
        'sold_ten', 'sold_fifteen', 'sold_twenty', 'sold_500', 'sold_700', 'sold_800', 'sold_900', 'sold_1000',
        'sold_1200', 'sold_1500')}),
        ('Permissions', {'fields': ('active', 'staff', 'admin')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'full_name')}
         ),
    )
    search_fields = ('full_name', 'email')
    ordering = ('email',)
    filter_horizontal = ()


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(City)
admin.site.register(Day)
admin.site.register(Sector)
admin.site.register(Row)
admin.site.register(Seat)
admin.site.register(Cache)
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
