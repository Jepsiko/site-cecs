from django.db import models


class Album(models.Model):
	name = models.CharField(max_length=200)
	pub_date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.name


class Photo(models.Model):
	album = models.ForeignKey(Album, on_delete=models.CASCADE)
	image = models.ImageField()
