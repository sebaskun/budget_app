# coding=utf-8
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
# from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError
from .models import Correlative
from ..resource.models import CategoryEquipment

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('email', 'name', 'lastname', 'image', 'password', 'is_active', 'is_admin',
                  'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin', 'view_image')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'lastname', 'image',)}),
        ('Permiso', {'fields': ('is_admin', 'is_superuser',
                      'groups', 'user_permissions')}),
    )
    # # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # # overrides get_fieldsets to use this attribute when creating a user.
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2')}
    #     ),
    # )


    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     (_(u'Datos personales'), {'fields': ('name', 'lastname', 'image')}),
    #     (_(u'Permisos'), {'fields': ('is_admin', 'is_superuser',)}),
    # )
    # # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None,
         {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    def view_image(self, obj):
        if obj.image:
            try:
                thumb_url = get_thumbnailer(obj.image)['avatar'].url
                return format_html(
                    """
                        <img src='{}'>
                    """, thumb_url)
            except InvalidImageFormatError:
                return "Sin imagen"
        else:
            return "Sin imagen"
    view_image.short_description = "Imagen"


@admin.register(Correlative)
class CorrelativeAdmin(admin.ModelAdmin):
    list_display = (
        "model", "prefix", "current_number"
    )

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(CategoryEquipment)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
