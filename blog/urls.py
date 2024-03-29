from django.urls import path, re_path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    re_path('news/detail/(?P<slug>[-\w]+)/$', views.ArticleDetailView.as_view(), name='article_detail'),
    re_path('news/category/(?P<slug>[-\w]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    path('news/like/<int:pk>/', views.like, name='like'),
    path('news/search/', views.search, name='search'),
]
