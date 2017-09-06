from django.shortcuts import render
from django.views.generic import ListView, TemplateView, FormView
from blog import models
from django.core.urlresolvers import reverse
from .forms import SuggestionForm
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from blog.views import SearchListView


class SuggestionFormView(FormView):
	template_name = 'about.html'
	form_class = SuggestionForm
	success_url = '/about'

	def form_valid(self, form):
		send_mail(
			'Suggestion from {}'.format(form.cleaned_data['name']),
	        form.cleaned_data['suggestion'],
	        '{name} <{email}>'.format(**form.cleaned_data),
	        ['vickeyakinmade22@gmail.com']
	    )
		messages.add_message(self.request, messages.SUCCESS,
                             'Thanks for your suggestion!')
		mail = models.Mail(
			name = form.cleaned_data['name'],
			email = form.cleaned_data['email'],
			message = form.cleaned_data['suggestion']
		)
		mail.save()
		return super(SuggestionFormView, self).form_valid(form)


def get_popular_posts():
	return models.Post.objects.filter(visibility=True).order_by('-views')[:2]


class AboutView(SuggestionFormView, TemplateView):
	template_name = 'about.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['popular'] = get_popular_posts()
		return context


class HomeView(ListView):
	context_object_name = "posts"
	template_name = 'home.html'
	paginate_by = 1

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['popular'] = get_popular_posts()
		return context

	def get_queryset(self, **kwargs):
		return models.Post.objects.filter(visibility=True).order_by('-created_at')