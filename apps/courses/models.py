from django.db import models
from django.utils.timezone import now
from apps.users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса")
    preview = models.ImageField(upload_to='course/', verbose_name='Превью')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса")
    preview = models.ImageField(upload_to='lesson/', verbose_name='Превью')
    video_link = models.URLField(verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Course', **NULLABLE,
                               related_name='lesson')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payments(models.Model):
    PAYMENT_TYPE = (
        ('cash', 'наличные'),
        ('transfer', 'перевод на счет')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date_payment = models.DateTimeField(default=now)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='урок', blank=True, null=True)
    payment_amount = models.FloatField(verbose_name='сумма оплаты')
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE, verbose_name='способ оплаты')
