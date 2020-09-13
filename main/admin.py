from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import get_object_or_404

from multiupload.admin import MultiUploadAdmin

from .models import Album, Photo, Account, Post, Event, Chant, Journal, PV


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


class PhotoInlineAdmin(admin.TabularInline):
	model = Photo


class AlbumMultiuploadMixing(object):
	def process_uploaded_file(self, uploaded, album, request):
		if album:
			image = Photo.objects.create(image=uploaded, album=album)
		else:
			image = Photo.objects.create(image=uploaded, album=None)
		return {
			'url': image.image.url,
			'thumbnail_url': image.image.url,
			'id': image.id,
		}


class AlbumAdmin(AlbumMultiuploadMixing, MultiUploadAdmin):
	list_display = ('name', 'pub_date')
	search_fields = ('name',)
	ordering = ('-pub_date',)
	inlines = [PhotoInlineAdmin, ]
	multiupload_form = True
	multiupload_list = False

	def delete_file(self, pk, request):
		'''
		Delete an image.
		'''
		obj = get_object_or_404(Photo, pk=pk)
		return obj.delete()


class PhotoAdmin(AlbumMultiuploadMixing, MultiUploadAdmin):
	multiupload_form = False
	multiupload_list = True
	multiupload_limitconcurrentuploads = 6


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)


class PostAdmin(admin.ModelAdmin):
	list_display = ('name', 'order')
	search_fields = ('name',)
	ordering = ('order',)


admin.site.register(Post, PostAdmin)


class ChantAdmin(admin.ModelAdmin):
	list_display = ('name', 'order')
	search_fields = ('name',)
	ordering = ('order',)


admin.site.register(Chant, ChantAdmin)


class EventAdmin(admin.ModelAdmin):
	list_display = ('name', 'pub_date')
	search_fields = ('name',)
	ordering = ('-pub_date',)


admin.site.register(Event, EventAdmin)


class JournalAdmin(admin.ModelAdmin):
	list_display = ('name', 'pub_date')
	search_fields = ('name',)
	ordering = ('-pub_date',)


admin.site.register(Journal, JournalAdmin)


class PVAdmin(admin.ModelAdmin):
	list_display = ('name', 'pub_date')
	search_fields = ('name',)
	ordering = ('-pub_date',)


admin.site.register(PV, PVAdmin)
