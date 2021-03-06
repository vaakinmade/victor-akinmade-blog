from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from datetime import datetime


class Post(models.Model):
	created_at = models.DateTimeField(default=datetime.now())
	title = models.CharField(max_length=225)
	author = models.ForeignKey(User)
	content = models.TextField()
	views = models.PositiveIntegerField(default=0)
	tags = models.CharField(max_length=225, default="")
	visibility = models.BooleanField(default=False)
	likes = models.IntegerField(default=0)
	image = models.ImageField(upload_to='images/blog', default='pic_folder/None/no-img.jpg')
	slug = models.SlugField(
        unique=True,
        default=get_random_string,
        max_length=50,
    )


	def __str__(self):
		return "{} by {}".format(self.title, self.author.username)

	def get_absolute_url(self):
   	    return reverse('home')

	def slug_title(self):
		return slugify(self.title)

	@property
	def total_likes(self):
		return self.likes.count()


class Mail(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=225)
	email = models.CharField(max_length=50)
	message = models.TextField()

	def __str__(self):
		return "Mail from " + self.name
