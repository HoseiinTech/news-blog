from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, View
from blog.models import Article, Category, Like
from django.http import JsonResponse
from django.db.models import Count, Q
from datetime import datetime, timedelta


class HomePageView(ListView):
    queryset = Article.objects.filter(status=True).order_by('-created')[:6]
    template_name = 'blog/home.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_week = datetime.today() - timedelta(days=7)
        context['last_week_articles'] = Article.objects.filter(status=True, articlehit__created__gte=last_week) \
            .annotate(count=Count('hits', filter=Q(articlehit__created__gt=last_week))
                      ).order_by('-count', '-created')
        return context


class ArticleDetailView(DetailView):
    context_object_name = 'articles'
    template_name = 'blog/articles_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.filter(status=True), slug=slug)

        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if self.request.user.likes.filter(article_id=self.object.id, user_id=self.request.user.id).exists():
                context['is_liked'] = True
            else:
                context['is_liked'] = False
        return context


class CategoryDetailView(ListView):
    context_object_name = 'articles'
    template_name = 'blog/category_detail.html'
    paginate_by = 2

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        articles = category.articles.filter(status=True).order_by('-created')
        return articles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetailView, self).get_context_data()
        slug = self.kwargs.get('slug')
        context['name_category'] = get_object_or_404(Category, slug=slug)
        return context


def like(request, pk):
    article = Article.objects.get(id=pk)
    if request.user.is_authenticated:
        try:
            like = Like.objects.get(article_id=pk, user_id=request.user.id)
            like.delete()
            return JsonResponse({'result': 'unliked'})
        except:
            Like.objects.create(article_id=pk, user_id=request.user.id)
            return JsonResponse({'result': 'liked'})
