from django.db import models
from django.contrib.auth.models import User

from .enums import NotificationCategories


class Author(models.Model):
    ROLE_CHOICES = (
        ("author", "Автор"),

        ('is', 'Сотрудники Комиссии ИС'),
        ('nma', 'Сотрудники Комиссии по НМА'),

        ('subd', 'Администратор СУБД'),
        ('sp', 'Администратор сервера приложений'),
        ('ib', 'Администратор информационной безопасности'),
        ('to', 'Специалист по техническому обслуживанию'),

        ('patentoved','Сотрудники ЦТТ. Патентовед'),
        ('urist', 'Сотрудники ЦТТ. Эксперт «Юрист»'),
        ('patent', 'Сотрудники ЦТТ. Эксперт «Патентный поверенный»'),
        ('manager', 'Сотрудники ЦТТ. Эксперт «Менеджер»'),

        ('other', 'Другое'),
        ('admin', 'Администратор'),
    )
    name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Имя')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", blank=True, null=True)
    role = models.CharField(max_length=128, choices=ROLE_CHOICES, blank=True, null=True, default='author',
                            verbose_name='Роль')
    address = models.CharField(max_length=256,blank=True,null=True,verbose_name='Адрес места жительства с указанием почтового индекса')
    post = models.CharField(max_length=128,blank=True,null=True,verbose_name='Должность, место работы')
    phone = models.CharField(max_length=128,blank=True,null=True,verbose_name='Телефон, Е-mail')
    snils = models.CharField(max_length=128,blank=True,null=True,verbose_name='СНИЛС')
    inn = models.CharField(max_length=128,blank=True,null=True,verbose_name='ИНН')
    
    class Meta:
        verbose_name_plural = 'Авторы'
        verbose_name = 'Автор'

    def __str__(self):
        return self.name


class Notifications(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    text = models.TextField(blank=True, null=True, verbose_name='Текст')
    category = models.CharField(max_length=3, choices=NotificationCategories.choices,
                                default=NotificationCategories.RID, blank=True, null=True)
    datetime_create = models.DateTimeField(verbose_name='Время создания', auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Уведомления'
        verbose_name = 'Уведомление'

    def __str__(self):
        return str(self.id)

    def get_category(self):
        return dict(NotificationCategories.choices)[self.category]