from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db import models


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Videos.Status.Published)


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Videos(models.Model):
    class Status(models.TextChoices):
        Draft = 'DF', 'Draft'
        Published = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    video = models.FileField(upload_to='courses/videos')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE
                                 )
    publish_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.Draft
                              )
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-publish_time"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail_page", args=[self.slug])


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.email


class Comment(models.Model):
    news = models.ForeignKey(Videos,
                             on_delete=models.CASCADE,
                             related_name='comments'
                             )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments'
                             )
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return f"Comment - {self.body} by {self.user} "


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    time_limit = models.PositiveIntegerField(default=60)

    def __str__(self):
        return self.name


class QuizResult(models.Model):
    user = models.ForeignKey('auth.User',
                             on_delete=models.CASCADE)  # Укажите, какая модель используется для пользователей
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    grade = models.PositiveIntegerField()
    time_spent = models.PositiveIntegerField()  # Время прохождения в секундах
    completed_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    answer_1 = models.CharField(max_length=255)
    answer_2 = models.CharField(max_length=255)
    answer_3 = models.CharField(max_length=255)
    answer_4 = models.CharField(max_length=255)
    correct_answer = models.PositiveSmallIntegerField(choices=[
        (1, 'Answer 1'),
        (2, 'Answer 2'),
        (3, 'Answer 3'),
        (4, 'Answer 4')
    ])

    def __str__(self):
        return self.text

    def get_answers(self):
        return [
            (1, self.answer_1),
            (2, self.answer_2),
            (3, self.answer_3),
            (4, self.answer_4),
        ]


class Yangi(models.Model):
    class Status(models.TextChoices):
        Draft = 'DF', 'Draft'
        Published = 'PB', 'Published'

    title = models.CharField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to='yangi/images')

    publish_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.Draft
                              )
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-publish_time"]

    def __str__(self):
        return self.title


class Termin(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.title


class Instrument(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title


class Kitoblar(models.Model):
    class Status(models.TextChoices):
        Draft = 'DF', 'Draft'
        Published = 'PB', 'Published'

    title = models.CharField(max_length=255)
    body = models.TextField()
    pdf = models.FileField(upload_to='courses/pdf')

    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.Draft)

    def __str__(self):
        return self.title
