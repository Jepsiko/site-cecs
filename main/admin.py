from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Album, Photo, Account, Post


class AccountAdmin(UserAdmin):
	list_display = ('first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_admin', 'is_member', 'post')
	search_fields = ('first_name', 'last_name', 'email')
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = [
		(None, {
			'fields': ('username', 'first_name', 'last_name', 'email', 'display_email', 'phone_number', 'display_phone_number', 'photo', 'description', 'is_member', 'date_joined', 'last_login')
		}),
		('Staff options', {
			'fields': ('post',),
		}),
		('Advanced options', {
			'classes': ('collapse',),
			'fields': ('is_staff', 'is_admin'),
		}),
	]

	ordering = ('first_name',)


admin.site.register(Account, AccountAdmin)


class PhotoInline(admin.TabularInline):
	model = Photo
	extra = 3


class AlbumAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {
			'fields': ('name', 'pub_date')
		}),
	]
	inlines = [PhotoInline]
	list_display = ('name', 'pub_date')
	list_filter = ['pub_date']
	search_fields = ['name']


admin.site.register(Album, AlbumAdmin)


class PostAdmin(admin.ModelAdmin):
	list_display = ('name', 'order', 'description')
	search_fields = ('name',)
	ordering = ('order',)


admin.site.register(Post, PostAdmin)
