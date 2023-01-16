from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from blog.models import Article, Category
from django.db.models import Count, Q
from datetime import datetime, timedelta


class HomePageView(ListView):
    queryset = Article.objects.filter(status=True).order_by('-created')[:4]
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
