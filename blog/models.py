from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import dateformat





class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
            .filter(status='published')


class Post(models.Model):
    """  """
    STATUC_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=250) # строка длиной максимум 20 символов
    post_img = models.ImageField(upload_to='images/', default='', null=True, blank=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish') #короткое url имя
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField() #основной контент
    publish = models.DateTimeField(default = timezone.now) #default - то что запишется, если не было передано других сведений
    created = models.DateTimeField(auto_now_add=True) #когда он был создан
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length= 10, choices = STATUC_CHOICES, default='draft')
    objects = models.Manager()
    published = PublishedManager()


    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args = [self.slug])

    class Meta:
        ordering =('-publish',)
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)
    def __str__(self):
        return f'Коментарий {self.name} on {self.post} '