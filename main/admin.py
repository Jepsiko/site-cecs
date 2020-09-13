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

# class AlbumAdmin(admin.ModelAdmin):
# 	fieldsets = [
# 		(None, {
# 			'fields': ('name', 'pub_date')
# 		}),
# 	]
# 	inlines = [PhotoInline]
# 	list_display = ('name', 'pub_date')
# 	list_filter = ['pub_date']
# 	search_fields = ['name']
#
#
# admin.site.register(Album, AlbumAdmin)
#
#
# class AlbumAdmin(MultiUploadAdmin):
# 	# default value of all parameters:
# 	change_form_template = 'multiupload/change_form.html'
# 	change_list_template = 'multiupload/change_list.html'
# 	multiupload_template = 'multiupload/upload.html'
# 	# if true, enable multiupload on list screen
# 	# generaly used when the model is the uploaded element
# 	multiupload_list = True
# 	# if true enable multiupload on edit screen
# 	# generaly used when the model is a container for uploaded files
# 	# eg: gallery
# 	# can upload files direct inside a gallery.
# 	multiupload_form = True
# 	# max allowed filesize for uploads in bytes
# 	multiupload_maxfilesize = 3 * 2 ** 20 # 3 Mb
# 	# min allowed filesize for uploads in bytes
# 	multiupload_minfilesize = 0
# 	# limit concurrent uploads in order to avoid timeouts (try 6–10 if experiencing problems)
# 	multiupload_limitconcurrentuploads = None
# 	# tuple with mimetype accepted
# 	multiupload_acceptedformats = ("image/jpeg", "image/png",)
#
# 	def process_uploaded_file(self, uploaded, object, request):
# 		'''
# 		Process uploaded file
# 		Parameters:
# 			uploaded: File that was uploaded
# 			object: parent object where multiupload is
# 			request: request Object
# 		Must return a dict with:
# 		return {
# 			'url': 'url to download the file',
# 			'thumbnail_url': 'some url for an image_thumbnail or icon',
# 			'id': 'id of instance created in this method',
# 			'name': 'the name of created file',
#
# 			# optionals
# 			"size": "filesize",
# 			"type": "file content type",
# 			"delete_type": "POST",
# 			"error" = 'Error message or jQueryFileUpload Error code'
# 		}
# 		'''
# 		# example:
# 		title = kwargs.get('title', [''])[0] or uploaded.name
# 		f = self.model(upload=uploaded, title=title)
# 		f.save()
# 		return {
# 			'url': f.image_thumb(),
# 			'thumbnail_url': f.image_thumb(),
# 			'id': f.id,
# 			'name': f.title
# 		}
#
# 	def delete_file(self, pk, request):
# 		'''
# 		Function to delete a file.
# 		'''
# 		# This is the default implementation.
# 		obj = get_object_or_404(self.queryset(request), pk=pk)
# 		obj.delete()
#
#
# admin.site.register(Album, AlbumAdmin)


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
	ordering = ('pub_date',)


admin.site.register(Event, EventAdmin)


class JournalAdmin(admin.ModelAdmin):
	list_display = ('name', 'pub_date')
	search_fields = ('name',)
	ordering = ('pub_date',)


admin.site.register(Journal, JournalAdmin)


class PVAdmin(admin.ModelAdmin):
	list_display = ('name', 'pub_date')
	search_fields = ('name',)
	ordering = ('pub_date',)


admin.site.register(PV, PVAdmin)
