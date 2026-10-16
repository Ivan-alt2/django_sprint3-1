from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TimestampModel(models.Model):
    is_published = models.BooleanField(
        _('Опубликовано'),
        default=True,
        help_text=_('Снимите галочку, чтобы скрыть публикацию.'),
    )
    created_at = models.DateTimeField(_('Добавлено'), auto_now_add=True)

    class Meta:
        abstract = True


class PublishedManager(models.Manager):
    """
    Менеджер для выборки только опубликованных записей,
    дата публикации которых уже наступила.
    """

    def get_queryset(self):
        now = timezone.now()
        return super().get_queryset().filter(
            is_published=True,
            pub_date__lte=now,
        )


class Category(TimestampModel):
    """Категория."""

    title = models.CharField(_('Заголовок'), max_length=256)
    description = models.TextField(_('Описание'), blank=True)
    slug = models.SlugField(
        _('Идентификатор'),
        max_length=64,
        unique=True,
        help_text=_(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        ),
    )

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('Категории')

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Location(TimestampModel):
    """Местоположение."""

    name = models.CharField(_('Название места'), max_length=256)

    class Meta:
        verbose_name = _('местоположение')
        verbose_name_plural = _('Местоположения')

    def __str__(self):
        return self.name


class Post(TimestampModel):
    """Публикация."""

    title = models.CharField(_('Заголовок'), max_length=256)
    text = models.TextField(_('Текст'))
    pub_date = models.DateTimeField(
        _('Дата и время публикации'),
        null=True,
        blank=True,
        help_text=_(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации. Оставьте пустым для черновика.'
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('Автор публикации'),
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name=_('Местоположение'),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name=_('Категория'),
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = _('публикация')
        verbose_name_plural = _('Публикации')
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
