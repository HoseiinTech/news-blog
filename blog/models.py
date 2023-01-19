from account.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify
from extensions.utils import jalali_converter

# <- Categories Model ->
STATUS_CATEGORY_CHOICES = {
    (True, 'فعال'),
    (False, 'غیرفعال')
}


class Category(models.Model):
    title = models.CharField(max_length=800, verbose_name='عنوان')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    status = models.BooleanField(default=True, choices=STATUS_CATEGORY_CHOICES, verbose_name='وضعیت')
    slug = models.SlugField(unique=True, null=True, editable=False, allow_unicode=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Category, self).save()

    def get_absolute_url(self):
        return reverse('blog:category_detail', args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


# <- IP Address Model ->
class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آیپی')


# <- Articles Model ->

TYPE_CHOICES = {
    (True, 'خبر ویژه'),
    (False, 'خبر معمولی'),
}

STATUS_ARTICLE_CHOICES = {
    (True, 'منتشر شده'),
    (False, 'منتشر نشده')
}


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='نویسنده')
    category = models.ManyToManyField(Category, related_name='articles', verbose_name='دسته بندی')
    title = models.CharField(max_length=250, verbose_name='عنوان',
                             help_text='عنوانی که برای خبر ها می گذارید نباید تکراری باشد.')
    description = RichTextField(verbose_name='توضیحات')
    short_description = models.TextField(verbose_name='پیشنمایش',
                                         help_text='این متن به عنوان خلاصه ای از محتوای مقاله شما در حداکثر یک بند می باشد.')
    image = models.ImageField(upload_to='media/images/articles', verbose_name='تصویر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    news_type = models.BooleanField(blank=True, null=True, default=False, verbose_name='نوع خبر', choices=TYPE_CHOICES,
                                    help_text=format_html(
                                        '<div id="id_short_description_helptext" class="help">اگر خبر شما جزو اخبار مهم و فوری می باشد می توانید آن را در دسته<strong style="margin:5px">ویژه</strong>قرار دهید.</div>'))
    status = models.BooleanField(default=True, verbose_name='وضعیت', choices=STATUS_ARTICLE_CHOICES)
    hits = models.ManyToManyField(IpAddress, through='ArticleHit', blank=True, related_name='hits',
                                  verbose_name='بازدید ها', editable=False)
    slug = models.SlugField(unique=True, null=True, editable=False, allow_unicode=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Article, self).save()

    def get_image(self):
        if self.image:
            return format_html(
                f'<img src="{self.image.url}" alt="{self.title}" style="height:65px;width:95px;border-radius:3px;"')
        return format_html('<h3>بدون تصویر</h3>')

    get_image.short_description = 'تصویر'

    def get_category(self):
        return ' , '.join([category.title for category in self.category.all()])

    get_category.short_description = 'دسته بندی'

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.slug])

    def jalali_date(self):
        return jalali_converter(self.created)

    jalali_date.short_description = 'تاریخ ایجاد'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


# <- through model (hits) ->
class ArticleHit(models.Model):
    articles = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IpAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='کاربر')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes', verbose_name='مقاله')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.article.title}'

    class Meta:
        ordering = ('-created',)
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک ها'
