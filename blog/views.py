from django.views.generic import CreateView, ListView, DetailView, FormView
from blog import models
from .mixins import PageTitleMixin, ImageOperations
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


class PostCreateView(PageTitleMixin, CreateView):
	template_name = 'blog/post_form.html'
	fields = ['title', 'content', 'image']
	model = models.Post	
	page_title = "New Blog Entry"

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(PostCreateView, self).form_valid(form)


class SearchListView(ListView):
	template_name = "search.html"
	context_object_name = "search_items"

	def get_queryset(self):
		query = SearchQuery(self.request.GET.get('q'))
		vector = SearchVector('title', 'content')
		rank_parameters = SearchRank(vector, query)
		if query:
			result = models.Post.objects.annotate(search=vector, rank=rank_parameters
				).filter(search=query).order_by('-rank')
			return result

	def get_context_data(self, **kwargs):
		context = super(SearchListView, self).get_context_data(**kwargs)
		context["search"] = self.request.GET.get('q')
		return context


class TagListView(PageTitleMixin, ListView):
	template_name = 'blog/tag_list.html'
	context_object_name = "tag_posts"
	page_title = ""

	def get_context_data(self, **kwargs):
		context = super(TagListView, self).get_context_data(**kwargs)
		context["tag"] = self.kwargs['tag']
		return context

	def get_queryset(self):
		return models.Post.objects.filter(tags__icontains=self.kwargs['tag'],
			visibility=True).order_by('-created_at')


class PostListView(PageTitleMixin, ListView):
	context_object_name = "posts"

	def get_context_data(self, **kwargs):
		context = super(PostListView, self).get_context_data(**kwargs)
		post_images = models.Post.objects.all()
		obj = ImageOperations()

		for post in post_images:
			obj.process_ratio(post.image)
		
		return context

	def get_queryset(self):
		return models.Post.objects.filter(visibility=True).order_by('-created_at')


class PostDetailView(PageTitleMixin, DetailView):
	model = models.Post

	def get_queryset(self):
		return models.Post.objects.filter(slug=self.kwargs['slug'])

	def get_context_data(self, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		self.resolve_slug()

		post_id = self.get_queryset().values_list('id', flat=True)[0]
		
		try:
			context['post_next'] = models.Post.objects.filter(id__gt=post_id).order_by('created_at')[0:1].get()
		except models.Post.DoesNotExist:
			context['post_next'] = None
		try:
			context['post_prev'] = models.Post.objects.filter(id__lt=post_id).order_by('-created_at')[0:1].get()
		except models.Post.DoesNotExist:
			context['post_prev'] = None

		tags = [tt for t in self.get_queryset().values_list('tags') for tt in t]
		context['tag_list'] = ", ".join(tags).split(", ")
		return context

	def resolve_slug(self):
		# Redirect if the slug does not match
		slug_title = slugify(self.get_queryset().values_list('title', flat=True)[0])
		if self.kwargs['slug_title'] != slug_title:
			return HttpResponseRedirect(reverse('blog:detail',
				kwargs={'slug': self.kwargs['slug'], 'slug_title': slug_title}))