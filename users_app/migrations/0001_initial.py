# Generated by Django 4.1.4 on 2022-12-23 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Имя')),
                ('role', models.CharField(blank=True, choices=[('author', 'Автор'), ('is', 'Сотрудники Комиссии ИС'), ('nma', 'Сотрудники Комиссии по НМА'), ('subd', 'Администратор СУБД'), ('sp', 'Администратор сервера приложений'), ('ib', 'Администратор информационной безопасности'), ('to', 'Специалист по техническому обслуживанию'), ('patentoved', 'Сотрудники ЦТТ. Патентовед'), ('urist', 'Сотрудники ЦТТ. Эксперт «Юрист»'), ('patent', 'Сотрудники ЦТТ. Эксперт «Патентный поверенный»'), ('manager', 'Сотрудники ЦТТ. Эксперт «Менеджер»'), ('other', 'Другое'), ('admin', 'Администратор')], default='author', max_length=128, null=True, verbose_name='Роль')),
                ('address', models.CharField(blank=True, max_length=256, null=True, verbose_name='Адрес места жительства с указанием почтового индекса')),
                ('post', models.CharField(blank=True, max_length=128, null=True, verbose_name='Должность, место работы')),
                ('phone', models.CharField(blank=True, max_length=128, null=True, verbose_name='Телефон, Е-mail')),
                ('snils', models.CharField(blank=True, max_length=128, null=True, verbose_name='СНИЛС')),
                ('inn', models.CharField(blank=True, max_length=128, null=True, verbose_name='ИНН')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст')),
                ('category', models.CharField(blank=True, choices=[('rid', 'РИД'), ('exp', 'Экспертиза')], default='rid', max_length=3, null=True)),
                ('datetime_create', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время создания')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users_app.author', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
            },
        ),
    ]
