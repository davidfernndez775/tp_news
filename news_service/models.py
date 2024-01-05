from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import misaka
from django.contrib.auth import get_user_model
User = get_user_model()  # nopep8
from django.utils import timezone

# Create your models here.


class Theme(models.Model):
    theme = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.theme


class Journalist(models.Model):
    # establecemos la relacion con la clase User de Django
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='journalist')
    # cambiamos el nombre del campo id(PrimaryKey) por defecto para evitar conflictos con el id de la clase User
    journalist_id = models.AutoField(primary_key=True, default=None)
    description = models.TextField(max_length=256)
    photo = models.ImageField(default='',
                              upload_to='images/profile_pictures')
    is_chief = models.BooleanField()
    slug = models.SlugField(allow_unicode=True, unique=True, editable=False)
    posts = models.ManyToManyField('Post', through='JournalistPost')

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        '''funcion que mejora la visualidad en la direccion del navegador'''
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.TextField(max_length=256)
    slug = models.SlugField(allow_unicode=True, unique=True, editable=False)
    author = models.ManyToManyField(Journalist, through='JournalistPost')
    image = models.ImageField(
        upload_to='images/news_pictures')
    content = models.TextField()
    content_html = models.TextField(editable=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField()
    theme = models.ForeignKey(
        Theme, related_name='themes', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    def publish_post(self):
        '''define la fecha de publicacion de un post'''
        self.publish_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        '''funcion que mejora la visualidad en la direccion del navegador'''
        self.slug = slugify(self.title)
        self.content_html = misaka.html(self.content)
        super().save(*args, **kwargs)

    def approve_post(self):
        '''aprueba un post'''
        self.approve = True
        self.save()

    def get_absolute_url(self):
        '''funcion por defecto para cuando termine de crear un post vaya a una url determinada'''
        return reverse("post_detail", kwargs={"slug": self.slug})

    class Meta:
        # definimos el orden en que queremos ver los grupos
        ordering = ['-publish_date']


class JournalistPost(models.Model):
    journalist = models.ForeignKey(
        Journalist, related_name='journalists', on_delete=models.CASCADE)
    posts = models.ForeignKey(
        Post, related_name='posts', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.journalist.username

    class Meta:
        # definimos una pareja de elementos que juntos deben ser unicos, por ejemplo en cada posts no pueden haber dos journalist con el mismo nombre
        unique_together = ('posts', 'journalist')


class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name='author', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post',
                             on_delete=models.CASCADE)
    content = models.TextField()
    content_html = models.TextField(editable=False)
    create_date = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField()

    def __str__(self) -> str:
        return self.content

    def save(self, *args, **kwargs):
        self.content_html = misaka.html(self.content)
        super().save(*args, **kwargs)

    def approve_comment(self):
        '''aprueba una comentario'''
        self.approve = True
        self.save()

    def get_absolute_url(self):
        '''funcion por defecto para cuando termine de crear un post vaya a una url determinada'''
        return reverse("comment_detail", kwargs={"pk": self.pk})

    def publish_comment(self):
        '''define la fecha de publicacion de un post'''
        self.publish_date = timezone.now()
        self.save()

    class Meta:
        # definimos el orden en el que queremos ver los posts
        ordering = ['-create_date']
        unique_together = ['user', 'content']
