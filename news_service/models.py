from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='journalist', primary_key=True)
    description = models.TextField(max_length=256)
    photo = models.ImageField(default='',
                              upload_to='images/profile_pictures')
    slug = models.SlugField(allow_unicode=True, unique=True, editable=False)
    posts = models.ManyToManyField('Post', through='JournalistPost')

    def __str__(self) -> str:
        return self.user.username

    def save(self, *args, **kwargs):
        '''funcion que mejora la visualidad en la direccion del navegador'''
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)


# Definimos un manager para las noticias aprobadas
class ApprovePostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(approve=True)


class Post(models.Model):
    title = models.TextField(max_length=256)
    slug = models.SlugField(allow_unicode=True, unique=True, editable=False)
    main_author = models.ForeignKey(
        Journalist, related_name='main_author', on_delete=models.CASCADE)
    other_authors = models.ManyToManyField(
        Journalist, through='JournalistPost', blank=True)
    image = models.ImageField(
        upload_to='images/news_pictures')
    content = models.TextField()
    content_html = models.TextField(editable=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField(default=False)
    theme = models.ForeignKey(
        Theme, related_name='themes', on_delete=models.CASCADE)

    # asignamos los managers, si agregamos managers personalizados tenemos que especificar el manager por defecto
    objects = models.Manager()
    approve_news = ApprovePostManager()

    # creamos los metodos de la clase Post

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

    def hide_post(self):
        '''quita la aprobacion de un post'''
        self.approve = False
        self.save()

    class Meta:
        # definimos el orden en que queremos ver los grupos
        ordering = ['-publish_date']


class JournalistPost(models.Model):
    journalist = models.ForeignKey(
        Journalist, related_name='journalists', on_delete=models.CASCADE)
    posts = models.ForeignKey(
        Post, related_name='posts', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.journalist.user.username

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


class Bulletin_Suscriptor(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)


# @receiver(post_save, sender=Post)
# def create_journalist(sender, instance, created, **kwargs):
#     if created:
#         print("Signal triggered!")
#         # Obtener el primer Journalist asociado al usuario
#         journalist = instance.main_author.username()

#         # Si hay un Journalist, asociarlo al Post
#         if journalist:
#             JournalistPost.objects.create(
#                 journalist=journalist, posts=instance)
