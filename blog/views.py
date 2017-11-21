from django.views.generic import CreateView, ListView, DetailView, UpdateView, View
from blog import models
from .mixins import PageTitleMixin, ImageOperationMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from hitcount.views import HitCountDetailView
import functools
import operator


class PostCreateView(PageTitleMixin, CreateView):
	template_name = 'blog/post_form.html'
	fields = ['title', 'content', 'image', 'tags', 'created_at']
	model = models.Post	
	page_title = "New Blog Entry"

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(PostCreateView, self).form_valid(form)


class PostUpdateView(PageTitleMixin, UpdateView):
    fields = ('title', 'content', 'image', 'tags')
    model = models.Post

    def get_page_title(self):
        obj = self.get_object()
        return 'Update {}'.format(obj.name)

    def get_success_url(self):
        return reverse('blog:update', kwargs={'slug': self.kwargs['slug']})


class SearchListView(ListView):
	context_object_name = "search_items"
	template_name = "blog/search.html"
	paginate_by = 5

	def get_queryset(self):
		search = self.request.GET.get('q')
		if search:
			terms = [SearchQuery(term) for term in search.split()]
			query = functools.reduce(operator.or_, terms)

			vector = SearchVector('title', 'content')			
			rank_parameters = SearchRank(vector, query)
		
			result = models.Post.objects.filter(visibility=True).annotate(
				search=vector, rank=rank_parameters
				).filter(search=query).order_by('-rank')
			return result
		return []

	def get_context_data(self, **kwargs):
		context = super(SearchListView, self).get_context_data(**kwargs)
		context["search"] = self.request.GET.get('q')
		return context


class TagListView(PageTitleMixin, ListView):
	template_name = 'blog/tag_list.html'
	context_object_name = "tag_posts"
	page_title = ""
	paginate_by = 5

	def get_context_data(self, **kwargs):
		context = super(TagListView, self).get_context_data(**kwargs)
		context["tag"] = self.kwargs['tag']
		return context

	def get_queryset(self):
		return models.Post.objects.filter(tags__icontains=self.kwargs['tag'],
			visibility=True).order_by('-created_at')


class PostLikeView(View):
	def get(self, request, *args, **kwargs):
		liked = False
		if self.request.method == 'GET':
		    post_id = self.request.GET['post_id']
		    post = models.Post.objects.get(id=int(post_id))
		    if self.request.session.get('has_liked_'+post_id, liked):
		        print("unlike")
		        if post.likes > 0:
		            likes = post.likes - 1
		            try:
		                del self.request.session['has_liked_'+post_id]
		            except KeyError:
		                print("keyerror")
		    else:
		        liked = request.session['has_liked_'+post_id] = True
		        likes = post.likes + 1
		        print("like", likes)
		post.likes = likes
		post.save()
		data = {}
		data['likes'], data['liked'] = likes, liked
		data = JsonResponse(data)
		return HttpResponse(data, content_type='application/json')


class  PostMixinDetailView(object):
	model = models.Post

	def get_queryset(self):
		return models.Post.objects.filter(slug=self.kwargs['slug'])

	def get_context_data(self, **kwargs):
		context = super(PostMixinDetailView, self).get_context_data(**kwargs)
		queryset = self.get_queryset()
		created_at = queryset.values_list('created_at', flat=True)[0]
		
		try:
			context['post_next'] = models.Post.objects.filter(created_at__gt=created_at,
				visibility=True).order_by('created_at')[0:1].get()
		except models.Post.DoesNotExist:
			context['post_next'] = None
		try:
			context['post_prev'] = models.Post.objects.filter(created_at__lt=created_at,
				visibility=True).order_by('-created_at')[0:1].get()
		except models.Post.DoesNotExist:
			context['post_prev'] = None

		tags = [t for t in queryset.values_list('tags', flat=True)]
		context['tag_list'] = ", ".join(tags).split(", ")

		image = queryset.values_list('image', flat=True)[:1]
		# enhanced_image = ImageOperationMixin().enhance("".join(image))
		context['liked'] = self.get_liked()
		return context

	def get_liked(self):
		queryset = self.get_queryset()
		post_id = queryset.values_list('id', flat=True)[0]
		liked = False
		if self.request.session.get('has_liked_'+str(post_id), liked):
		    liked = True
		return liked


class PostDetailView(PostMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view.
    """
    count_hit = True
   