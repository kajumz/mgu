from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationCategories(models.TextChoices):
    RID = 'rid', _('РИД')
    EXPERTIZE = 'exp',_('Экспертиза')

