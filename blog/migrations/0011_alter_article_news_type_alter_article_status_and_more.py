# Generated by Django 4.1.1 on 2022-09-30 17:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0010_alter_article_news_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='news_type',
            field=models.BooleanField(blank=True, choices=[(True, 'خبر ویژه'), (False, 'خبر معمولی')], default=False,
                                      help_text='<div id="id_short_description_helptext" class="help">اگر خبر شما جزو اخبار مهم و فوری می باشد می توانید آن را در دسته<strong style="margin:5px">ویژه</strong>قرار دهید.</div>',
                                      null=True, verbose_name='نوع خبر'),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.BooleanField(choices=[(False, 'منتشر نشده'), (True, 'منتشر شده')], default=True,
                                      verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.BooleanField(choices=[(True, 'فعال'), (False, 'غیرفعال')], default=True, verbose_name='وضعیت'),
        ),
    ]
