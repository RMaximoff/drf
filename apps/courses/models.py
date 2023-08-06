from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса")
    preview = models.ImageField(upload_to='course/', verbose_name='Превью', blank=False)


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса")
    preview = models.ImageField(upload_to='lesson/', verbose_name='Превью', blank=False)
    video_link = models.URLField(verbose_name='Ссылка на видео')

