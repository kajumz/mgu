from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ria_app.models import *
from users_app.forms import ReestrForm
from users_app.models import *


class ReestrView(LoginRequiredMixin, TemplateView):
    template_name = 'users_app/reestr.html'

    def get_context_data(self, **kwargs):
        context = super(ReestrView, self).get_context_data()
        context['active_button'] = 'reestr'


class ReestrDetailView(DetailView):
    model = Reestr
    template_name = 'users_app/reestr/reestr_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Информациия об объекте реестра'
        context['authors'] = self.get_ria_authors(self.object.ria)
        return context

    def get_ria_authors(self, ria):
        authors_ria_objects = AuthorsRIA.objects.filter(ria=ria)
        authors = [aro.author for aro in authors_ria_objects]
        return authors


class ReestrUpdateView(UpdateView):
    model = Reestr
    form_class = ReestrForm
    template_name = 'users_app/reestr/reestr_update_form.html'

    def get_success_url(self):
        return reverse('reestr')

    def get_context_data(self, **kwargs):
        context = super(ReestrUpdateView, self).get_context_data()
        context['page_name'] = 'Изменение объекта реестра'
        return context


class ReestrList(APIView):
    def get(self, request):
        objects = Reestr.objects.all()
        data = {
            "total": objects.count(),
            "totalNotFiltered": objects.count(),
        }
        rows = []
        for obj in objects:
            temp_ = {
                "pk": self.get_link_reestr(obj),
                "name_ria": self.get_name_link_ria(obj.ria),
                "pk_ria": self.get_pk_link_ria(obj.ria),
                "number_query_into_rospatent": obj.number_query_into_rospatent,
                "number_of_the_order_establishing_the_confidentiality_regime": obj.number_of_the_order_establishing_the_confidentiality_regime,
                "patent_number_certificate": obj.patent_number_certificate,
                "payment_document_number_on_payment_of_the_fee": obj.payment_document_number_on_payment_of_the_fee,
                "number_sz_for_payment_of_the_fee": obj.number_sz_for_payment_of_the_fee,
                "mpk_mkpo_mkty": obj.mpk_mkpo_mkty,
                "year_of_patent_validity": obj.year_of_patent_validity,
                "date_decision": self.get_link_date_decision(obj.decision),
                "date_of_issue_of_the_patent_certificate": obj.date_of_issue_of_the_patent_certificate,
                "patent_expiration_date": obj.patent_expiration_date,
                "date_of_filing_an_application_with_rospatent": obj.date_of_filing_an_application_with_rospatent,
                "date_of_the_order_to_establish_the_confidentiality_regime": obj.date_of_the_order_to_establish_the_confidentiality_regime,
                "date_ria": self.get_link_date_ria(obj.ria),
                "footing_ria": self.get_link_footing_ria(obj.ria.footing),
                "input_documents": obj.input_documents,
                "output_documents": obj.output_documents,
                "last_document": obj.last_document,
                'copyright_holder': obj.copyright_holder,
                "devision_ria": self.get_devision_ria(obj.ria),
                "type_ria": self.get_link_type_ria(obj.ria),
                "the_amount_of_royalties_paid_including_personal_income_tax": obj.the_amount_of_royalties_paid_including_personal_income_tax,
                "the_amount_of_income_from_the_use_and_disposal_of_the_rid": obj.the_amount_of_income_from_the_use_and_disposal_of_the_rid,
                'book_value': obj.ria.price,
                "accrued_depreciation_thousand_rubles": obj.accrued_depreciation_thousand_rubles,
                "the_amount_of_the_fee": obj.the_amount_of_the_fee,
                "term_of_payment_of_the_fee": obj.term_of_payment_of_the_fee,
                "the_deadline_for_responding_to_correspondence": obj.the_deadline_for_responding_to_correspondence,
                "countries_of_issue_of_the_patent": obj.countries_of_issue_of_the_patent,
                "approved_form_of_protection": obj.approved_form_of_protection,
                'authors_ria': self.get_link_authors_ria(obj.ria),
                "information_about_making_changes_to_the_registry": obj.information_about_making_changes_to_the_registry,
                'note': obj.note,
            }
            rows.append(temp_)
        data['rows'] = rows
        return Response(data)

    def get_link_reestr(self, obj):
        lazy = reverse_lazy('reestr-detail', args=(obj.pk,))
        html_ = format_html("<a href='{}'>{}</a>", lazy, obj.pk)
        return html_

    def get_pk_link_ria(self, ria):
        lazy = reverse_lazy('ria_info_view', args=(ria.pk,))
        html_ = format_html("<a href='{}'>{}</a>", lazy, ria.pk)
        return html_

    def get_name_link_ria(self, ria):
        lazy = reverse_lazy('ria_info_view', args=(ria.pk,))
        html_ = format_html("<a href='{}'>{}</a>", lazy, ria.name)
        return html_

    def get_link_date_decision(self, decision):
        if decision:
            lazy = reverse_lazy('exp_info_view', args=(decision.pk,))
            html_ = format_html("<a href='{}'>{}</a>", lazy, decision.date)
            return html_
        else:
            return ""

    def get_link_date_ria(self, ria):
        lazy = reverse_lazy('ria_info_view', args=(ria.pk,))
        html_ = format_html("<a href='{}'>{}</a>", lazy, ria.date_create)
        return html_

    def get_link_footing_ria(self, footing):
        if footing:
            lazy = reverse_lazy('footing_info', args=(footing.pk,))
            html_ = format_html("<a href='{}'>{}</a>", lazy, footing.type)
            return html_
        else:
            return ""

    def get_devision_ria(self, ria):
        lazy = reverse_lazy('ria_info_view', args=(ria.pk,))
        html_ = format_html("<a href='{}'>{}</a>", lazy, ria.get_division_display())
        return html_

    def get_link_type_ria(self, ria):
        lazy = reverse_lazy('ria_info_view', args=(ria.pk,))
        html_ = format_html("<a href='{}'>{}</a>", lazy, ria.get_type_display())
        return html_

    def get_link_authors_ria(self, ria):
        authors_ria_objects = AuthorsRIA.objects.filter(ria=ria)
        authors = [aro.author for aro in authors_ria_objects]
        html = ""
        for author in authors:
            lazy = reverse_lazy('author_detail', args=(author.pk,))
            html_ = format_html("<a href='{}'>{}</a>\n", lazy, author.name)
            html += html_
        return html
