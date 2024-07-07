import django_tables2 as tables
from django.urls import reverse_lazy

from ria_app.models import *
from django.utils.html import format_html

from django_tables2.utils import Accessor


class RIATable(tables.Table):
    class Meta:
        model = RIA
        fields = ('id', 'name', 'authors', 'division', 'main_ctt_worker', 'status')
        attrs = {"class": "table"}
        template_name = "django_tables2/bootstrap4.html"

    def render_id(self, value):
        lazy = reverse_lazy('ria_info_view', args=(value,))
        return format_html("<a href='{}'>{}</a>", lazy, value)

    def render_authors(self, value):
        names = []
        for v in value:
            name = Author.objects.get(pk=v['author_pk']).name
            names.append(name)
        text = '<br>'.join(names)
        return format_html(text)


class ActiveExpertiseTable(tables.Table):
    id_ = tables.Column(verbose_name='Решение', accessor=Accessor('id'))
    ria_id = tables.Column(verbose_name='РИД', accessor=Accessor('ria.id'))
    status = tables.Column(verbose_name='Статус', accessor=Accessor('status'))
    class Meta:
        model = Decision
        fields = ('id_','type', 'ria_id', 'status')
        template_name = "django_tables2/bootstrap4.html"

    def render_id_(self, value):
        lazy = reverse_lazy('exp_info_view', args=(value,))
        return format_html("<a href='{}'>{}</a>", lazy, value)

    def render_ria_id(self, value):
        lazy = reverse_lazy('ria_info_view', args=(value,))
        return format_html("<a href='{}'>{}</a>", lazy, value)
