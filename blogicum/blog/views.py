from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from blog.models import Post, Category


def get_published_posts(posts: QuerySet = Post.objects.all()):
    return posts.select_related(
        'category', 'location', 'author'
    ).filter(
        pub_date__lt=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    return render(
        request, 'blog/index.html',
        {'posts': get_published_posts()[:5]})


def post_detail(request, post_id):
    return render(
        request, 'blog/detail.html',
        {'post': get_object_or_404(get_published_posts(), pk=post_id)})


def category_posts(request, category_slug):
    try:
        category = get_published_posts(Category.objects.all()).get(slug=category_slug)
    except Category.DoesNotExist:
        raise Http404("Категория не найдена")
    
    posts = get_published_posts(category.posts.all())

    return render(
        request,
        'blog/category.html',
        {'category': category, 'posts': posts}
    )
#        'posts': get_published_posts(Post.objects.filter(category=category))})
