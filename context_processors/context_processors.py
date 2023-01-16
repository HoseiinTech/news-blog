from blog.models import Category, Article


def context(request):
    categories = Category.objects.filter(status=True)
    recent_article = Article.objects.filter(status=True).order_by('-created')[:4]
    return {'categories': categories, 'recent_article_side': recent_article}
