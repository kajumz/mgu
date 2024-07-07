from django.db import models
from users_app.models import Author, Notifications
from users_app.enums import NotificationCategories
from django.contrib.postgres.fields import ArrayField
from core import enums


class Footing(models.Model):
    type = models.CharField(max_length=3, verbose_name='Тип основания',
                            choices=enums.FootingType.choices, default=enums.FootingType.CONTRACT)
    data = models.JSONField(verbose_name='Сведения', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Учет оснований для создания РИД'
        verbose_name = 'Учет оснований для создания РИД'

    def __str__(self):
        if self.type == enums.FootingType.CONTRACT:
            return self.data['Номер и дата контракта']
        elif self.type == enums.FootingType.PLAN:
            return self.data['Руководитель ФИО, должность, ученая степень']
        elif self.type == enums.FootingType.QUEST:
            return self.data['Описание задания']
        elif self.type == enums.FootingType.OTHER:
            return self.data['Описание']


class RIA(models.Model):
    type = models.CharField(max_length=3, blank=True, null=True, verbose_name='Вид РИД', choices=enums.TypeRIA.choices,
                            default=enums.TypeRIA.COMPOSITION, )
    name = models.CharField(max_length=258, blank=True, null=True, verbose_name='Наименование РИД')
    division = models.CharField(max_length=128, blank=True, null=True, verbose_name='Подразделение',
                                choices=enums.DivisionRIA.choices, default=enums.DivisionRIA._1)
    price = models.IntegerField(default=0, blank=True, null=True, verbose_name='Первоначальная стоимость РИД')
    documentation = models.CharField(max_length=258, blank=True, null=True,
                                     verbose_name='Подразделение, где хранится контрольный экземпляр документации')
    footing = models.ForeignKey(Footing, blank=True, null=True, on_delete=models.CASCADE,
                                verbose_name='Основание для создания РИД')
    entities = models.CharField(max_length=258, blank=True, null=True,
                                verbose_name='Сведения о ранних раскрытиях сущности РИД')
    dependencies = models.CharField(max_length=258, blank=True, null=True, verbose_name='Сведения о зависимостях РИД')
    rospatent = models.CharField(max_length=258, blank=True, null=True, verbose_name='Сведения о Заявке в Роспатент')
    payment_schedule = models.CharField(max_length=258, blank=True, null=True,
                                        verbose_name='Сведения о графике оплаты пошлин в Роспатент')
    payment_dutes = models.CharField(max_length=258, blank=True, null=True, verbose_name='Сведения по оплатам пошлин')
    accounting = models.CharField(max_length=258, blank=True, null=True,
                                  verbose_name='Сведения о постановке РИД на бухгалтерский учет')
    document_information = models.CharField(max_length=258, blank=True, null=True,
                                            verbose_name='Подтверждающие документы')
    document_information_files = models.FileField('Файлы подтверждающих документов', upload_to='mydocs/', blank=True,
                                                  null=True)

    journal = ArrayField(models.JSONField(), verbose_name='Журнал выполненных пользователями действий', blank=True,
                         null=True)
    main_ctt_worker = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Ответственный сотрудник ЦТТ',
                                        blank=True, null=True, related_name='main_ctt_worker')
    status = models.CharField(max_length=256, blank=True, null=True, verbose_name='Статус',
                              choices=enums.RIAStatus.choices)
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Информация о РИД'
        verbose_name = 'Информация о РИД'

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        all_ctt = Author.objects.filter(role='author')
        for ctt in all_ctt:
            Notifications.objects.create(user=ctt, text='Создан новый РИД.', category=NotificationCategories.RID)
        super(RIA, self).save(*args, **kwargs)


class Contracts(models.Model):
    rid = models.ForeignKey(RIA, on_delete=models.CASCADE, blank=True, null=True)
    holder = models.CharField(max_length=258, blank=True, null=True, verbose_name='Сведения о правообладателе')
    recipient = models.CharField(max_length=258, blank=True, null=True, verbose_name='Сведения о получателе')
    number = models.CharField(max_length=258, blank=True, null=True, verbose_name='Номер договора')
    date = models.CharField(max_length=258, blank=True, null=True, verbose_name='Дата договора')
    period = models.CharField(max_length=258, blank=True, null=True, verbose_name='Срок действия договора')
    retribution = models.CharField(max_length=258, blank=True, null=True,
                                   verbose_name='Сумма вознаграждения по договору')
    target = models.CharField(max_length=258, blank=True, null=True, verbose_name='Цель заключения договора')
    object_info = models.CharField(max_length=258, blank=True, null=True,
                                   verbose_name='Сведения по объектам распоряжения правами')
    payment_schedule = models.CharField(max_length=258, blank=True, null=True,
                                        verbose_name='График платежей, для возмездных договоров')
    payment_info = models.CharField(max_length=258, blank=True, null=True, verbose_name='Сведения по платежам')
    rospatent_info = models.CharField(max_length=258, blank=True, null=True,
                                      verbose_name='Сведения о регистрации договора в Роспатенте')
    commission_decision = models.CharField(max_length=258, blank=True, null=True,
                                           verbose_name='Сведения по согласованию и принятом Комиссией ИС решении')
    journal = ArrayField(models.JSONField(), verbose_name='Журнал выполненных пользователями действий', blank=True,
                         null=True)

    class Meta:
        verbose_name_plural = 'Учет договоров'
        verbose_name = 'Учет договоров'

    def __str__(self):
        return str(self.holder)


class Decision(models.Model):
    TYPE_CHOICES = (
        ('a', 'Согласование Экспертизы ЦТТ по РИД'),
        ('aa', 'Повторное Согласование Экспертизы ЦТТ по РИД'),
        ('b', 'Согласование Решения о необходимости правовой охраны РИД'),
        ('c', 'Согласование Решения Комиссии НМА'),
        ('d', 'Согласование Решения Комиссии о досрочном прекращении действия ОИС'),
        ('e', 'Согласование Решения Комиссии о продлении действия ОИС'),
        ('f', 'Согласование Решения Комиссии о восстановлении прав на ОИС'),
        ('g', 'Согласование договора распоряжения правом'),
    )
    STATUS_CHOICES = (
        ('a', 'На рассмотрении экспертами'),
        ('b', 'Все эксперты приняли решения'),
        ('c', 'Закрыто положительно'),
        ('d', 'Закрыто отрицательно')
    )
    type = models.CharField(max_length=258, blank=True, null=True, choices=TYPE_CHOICES,
                            verbose_name='Тип Согласования')
    information_agenda = models.CharField(max_length=258, blank=True, null=True, verbose_name='Сведения по повестке')
    information_stage = ArrayField(models.JSONField(), verbose_name='Сведения по этапам согласования', blank=True,
                                   null=True)
    ria = models.ForeignKey(RIA, on_delete=models.CASCADE, blank=True, null=True, verbose_name='РИД')
    status = models.CharField(max_length=256, blank=True, null=True, verbose_name='Статус', choices=STATUS_CHOICES)
    date = models.DateField(verbose_name='Дата', auto_now=True)

    class Meta:
        verbose_name_plural = 'Учет Согласований и Решений'
        verbose_name = 'Учет Согласований и Решений'

    def __str__(self):
        return str(self.information_agenda)


class DocumentFilesRIA(models.Model):
    rid = models.ForeignKey(RIA, on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField('Document', upload_to='docs/', blank=True, null=True)

    def __str__(self):
        return str(self.file).split('/')[-1]


class AuthorsRIA(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Пользователь')
    ria = models.ForeignKey(RIA, on_delete=models.CASCADE, verbose_name='РИД')
    percent = models.IntegerField(verbose_name='Процент участия', default=100)


class Reestr(models.Model):
    ria = models.ForeignKey(RIA, on_delete=models.CASCADE, verbose_name='РИД')
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE, verbose_name='Решение комиссии', blank=True,
                                 null=True)
    number_query_into_rospatent = models.CharField(max_length=256, blank=True, null=True,
                                                   verbose_name='№ заявки в Роспатент')
    number_of_the_order_establishing_the_confidentiality_regime = models.CharField(max_length=256, blank=True,
                                                                                   null=True,
                                                                                   verbose_name='№ приказа установления режима конфиденциальности')
    patent_number_certificate = models.CharField(max_length=256, blank=True,
                                                 null=True,
                                                 verbose_name='№ патента, свидетельства')
    payment_document_number_on_payment_of_the_fee = models.CharField(max_length=256, blank=True,
                                                                     null=True,
                                                                     verbose_name='№ платежного документа об оплате пошлины')
    number_sz_for_payment_of_the_fee = models.CharField(max_length=256, blank=True,
                                                        null=True,
                                                        verbose_name='№ СЗ на оплату пошлины')
    mpk_mkpo_mkty = models.CharField(max_length=256, blank=True,
                                     null=True,
                                     verbose_name='МПК (для ИЗ и ПМ), МКПО (для ПО), МКТУ (для ТЗ)')
    year_of_patent_validity = models.CharField(max_length=256, blank=True,
                                               null=True,
                                               verbose_name='Год действия патента')
    date_of_issue_of_the_patent_certificate = models.CharField(max_length=256, blank=True,
                                                               null=True,
                                                               verbose_name='Дата выдачи патента, свидетельства')
    patent_expiration_date = models.CharField(max_length=256, blank=True,
                                              null=True,
                                              verbose_name='Дата окончания действия патента')
    date_of_filing_an_application_with_rospatent = models.CharField(max_length=256, blank=True,
                                                                    null=True,
                                                                    verbose_name='Дата подачи заявки в Роспатент')
    date_of_the_order_to_establish_the_confidentiality_regime = models.CharField(max_length=256, blank=True,
                                                                                 null=True,
                                                                                 verbose_name='Дата приказа установления режима конфиденциальности')
    input_documents = models.CharField(max_length=256, blank=True,
                                       null=True,
                                       verbose_name='Входящие документы')
    output_documents = models.CharField(max_length=256, blank=True,
                                        null=True,
                                        verbose_name='Исходящие документы')
    last_document = models.CharField(max_length=256, blank=True,
                                     null=True,
                                     verbose_name='Последний документ')
    copyright_holder = models.CharField(max_length=256, blank=True,
                                        null=True,
                                        verbose_name='Правообладатель')
    the_amount_of_royalties_paid_including_personal_income_tax = models.CharField(max_length=256, blank=True,
                                                                                  null=True,
                                                                                  verbose_name='Размер выплаченного авторского вознаграждения, включая НДФЛ')
    the_amount_of_income_from_the_use_and_disposal_of_the_rid = models.CharField(max_length=256, blank=True,
                                                                                 null=True,
                                                                                 verbose_name='Размер дохода от использования и распоряжения РИД')
    accrued_depreciation_thousand_rubles = models.CharField(max_length=256, blank=True,
                                                            null=True,
                                                            verbose_name='Начисленная амортизация (износ), тыс. руб.')
    the_amount_of_the_fee = models.CharField(max_length=256, blank=True,
                                             null=True,
                                             verbose_name='Размер пошлины')
    term_of_payment_of_the_fee = models.CharField(max_length=256, blank=True,
                                                  null=True,
                                                  verbose_name='Срок оплаты пошлины')
    the_deadline_for_responding_to_correspondence = models.CharField(max_length=256, blank=True,
                                                                     null=True,
                                                                     verbose_name='Срок ответа на корреспонденцию')
    countries_of_issue_of_the_patent = models.CharField(max_length=256, blank=True,
                                                        null=True,
                                                        verbose_name='Страны выдачи патента')
    approved_form_of_protection = models.CharField(max_length=256, blank=True,
                                                   null=True,
                                                   verbose_name='Утвержденная форма охраны')
    information_about_making_changes_to_the_registry = models.TextField(blank=True,
                                                                        null=True,
                                                                        verbose_name='Сведения о внесении изменений в реестр')
    note = models.CharField(max_length=256, blank=True,
                            null=True,
                            verbose_name='Примечание')

    class Meta:
        verbose_name = "Реестр"
        verbose_name_plural = "Реестры"
