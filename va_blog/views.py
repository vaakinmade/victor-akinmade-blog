from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from blog import models
from django.core.urlresolvers import reverse


class HomeView(ListView):
	context_object_name = "posts"
	template_name = 'home.html'
	paginate_by = 1

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def get_queryset(self, **kwargs):
		return models.Post.objects.filter(visibility=True).order_by('-created_at')


class AboutView(TemplateView):
	template_name = 'about.html'
