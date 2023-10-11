from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class MasterDictionaries(models.Model):
    word = models.CharField(max_length=46, verbose_name='слово', db_index=True)
    translation = models.CharField(max_length=50, verbose_name='перевод')

    def __str__(self) -> str:
        return self.word
    
    class Meta:
        verbose_name = 'Слово в словарь'
        verbose_name_plural = 'Главный словарь'


class UserDictionaries(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(MasterDictionaries, on_delete=models.CASCADE)
    last_training_date = models.DateTimeField(verbose_name='последняя тренировка', default=timezone.now)
    last_training_result = models.BooleanField(verbose_name='результат последней тренировки', default=False)

    def __str__(self) -> str:
        return f'{self.user} - {self.word}'
    
    class Meta:
        ordering = ['last_training_result', '-last_training_date']
        verbose_name = 'Словарь пользователя'
        verbose_name_plural = 'Словари пользователей'


class DatesLastAddedWordInUserDict(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_last_added_word = models.DateTimeField(verbose_name='последнее слово добавлено')

    def __str__(self) -> str:
        return f'{self.user} - {self.date_last_added_word}'
    
    class Meta:
        verbose_name = 'Дата полседнего добавления слова в словарь пользователя'
        verbose_name_plural = 'Даты полседнего добавления слова в словарь пользователей'