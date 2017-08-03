from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create/$', views.PostCreateView.as_view(), name='create'),
    url(r'^tag/(?P<tag>[\w-]+)/$', views.TagListView.as_view(), name='tag-search'),
    url(r'^search/$', views.SearchListView.as_view(), name='search'),
    url(r'^(?P<slug>.+)/(?P<slug_title>[\w-]+)?/$', views.PostDetailView.as_view(), name='detail'),
]