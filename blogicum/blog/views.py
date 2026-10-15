from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from blog.models import Post, Category
from django.db.models import QuerySet


def get_published_posts(posts: QuerySet | None = None) -> QuerySet:
    if posts is None:
        posts = Post.objects.all()

    return posts.select_related(
        "category",
        "location",
        "author",
    ).filter(
        pub_date__lt=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


def index(request):
    posts = get_published_posts()[:5]
    return render(request, "blog/index.html", {"posts": posts})


def post_detail(request, post_id):
    post = get_object_or_404(get_published_posts(), pk=post_id)
    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug,
    )
    posts = get_published_posts(category.posts.all())
    return render(
        request,
        "blog/category.html",
        {"category": category, "posts": posts},
    )
