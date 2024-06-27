import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django_tables2 import RequestConfig
from django.template.loader import render_to_string
from django.utils.html import format_html

from rest_framework.views import APIView
from rest_framework.response import Response

from users_app.forms import *
from ria_app.models import *
from users_app.tables import *
from users_app.decorators import *
from core import enums


@login_required
def account_view(request):
    account = Author.objects.get(user=request.user)
    form = AccountEditForm(instance=account)
    if request.POST:
        form = AccountEditForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            # name_ = form.cleaned_data.get('name')
            # address = form.cleaned_data.get('address')
            # post = form.cleaned_data.get('post')
            # phone = form.cleaned_data.get('phone')
            # snils = form.cleaned_data.get('snils')
            # inn = form.cleaned_data.get('inn')
            #
            # account.name = name_
            # account.address = address
            # account.post = post
            # account.phone = phone
            # account.snils = snils
            # account.inn = inn
            #
            # account.save()
            return redirect(account_view)
    context = {
        'active_button': 'settings',
        'form': form,
        'author_rias': AuthorsRIA.objects.filter(author=account)
    }
    return render(request, 'users_app/account.html', context=context)


def registration_view(request):
    sign_up_form = SignUpForm()
    context = {
        "sign_up_form": sign_up_form
    }
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password1'))
            Author.objects.create(name=username, user=user)
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('account'))
        else:
            context['not_valid_form'] = True
    return render(request, 'users_app/registration.html', context=context)


def user_auth_view(request):
    auth_form = AuthForm()
    context = {
        "auth_form": auth_form
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            context['not_found_user'] = True
        else:
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('account'))

    return render(request, 'users_app/auth.html', context=context)


@user_passes_test(ctt_or_admin_role_check)
def add_rid_view(request):
    create_ria_form = CreateRIAForm()
    all_author = Author.objects.filter(role='author')
    authors = [{'id': author.pk, 'name': author.name} for author in all_author]

    all_footing = Footing.objects.all()
    footings = []
    for footing in all_footing:
        footing_data = footing.data
        if footing.type == enums.FootingType.CONTRACT:
            footings_ = [footing_data['Номер и дата контракта'],
                         footing_data['Предмет контракта/договора'],
                         footing_data['Заказчик'],
                         footing_data['Тип договора'],
                         footing_data['Подразделение']]
            footing_data_str = ' '.join(footings_)
            footings.append({
                'id':footing.pk,
                'name':footing_data_str
            })
        elif footing.type == enums.FootingType.PLAN:
            footings_ = [footing_data['Направление'],
                         footing_data['Подразделение'],
                         footing_data['Шифр темы'],
                         footing_data['Руководитель ФИО, должность, ученая степень']
                         ]
            footing_data_str = ' '.join(footings_)
            footings.append({
                'id': footing.pk,
                'name': footing_data_str
            })
        elif footing.type == enums.FootingType.QUEST:
            footings_ = [footing_data['Описание задания'],
                         footing_data['Подразделение'],
                         footing_data['Кем дано задание ФИО, должность, ученая степень']
                         ]
            footing_data_str = ' '.join(footings_)
            footings.append({
                'id': footing.pk,
                'name': footing_data_str
            })
        elif footing.type == enums.FootingType.OTHER:
            footings_ = [footing_data['Описание']
                         ]
            footing_data_str = ' '.join(footings_)
            footings.append({
                'id': footing.pk,
                'name': footing_data_str
            })
    free_contracts = Contracts.objects.filter(rid=None)
    context = {
        'active_button': 'create_ria_form',
        'create_ria_form': create_ria_form,
        'authors': authors,
        'free_contracts': free_contracts,
        'footings':footings,
    }

    if request.method == 'POST':
        form = CreateRIAForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.status = enums.RIAStatus.A

            # journal
            journal_ = {
                "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "user": request.user.username,
                "action": "Создал РИД"
            }
            obj.journal = [journal_]

            # authors
            for name, percent in zip(request.POST.getlist('last_name'), request.POST.getlist('percent')):
                author = Author.objects.filter(name=name)[0]
                data = {
                    'author': author,
                    'ria': obj,
                    'percent': percent,
                }
                AuthorsRIA.objects.create(**data)

            obj.save()

            Reestr.objects.create(ria=obj)

            # files
            files = request.FILES.getlist('document_information_files')
            for f in files:
                DocumentFilesRIA.objects.create(rid=obj, file=f)

            # contract
            contract_pk = request.POST.get('contract_pk')
            if contract_pk:
                contract = Contracts.objects.get(pk=contract_pk)
                contract.rid = obj
                contract.save()
            return redirect('notifications')

    return render(request, 'users_app/create_ria_form.html', context=context)


@user_passes_test(ctt_or_admin_role_check)
def create_author_view(request):
    form = CreateAuthorForm()
    context = {
        'form': form
    }
    if request.POST:
        form = CreateAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_rid_view')
    return render(request, 'users_app/create_author.html', context=context)


@login_required
def notifications(request):
    table = RIATable(RIA.objects.all())
    RequestConfig(request).configure(table)
    context = {
        'rias': table,
        'active_button': 'notifications',
    }
    return render(request, 'users_app/notification.html', context)


@user_passes_test(ctt_or_admin_role_check)
def create_footing_view(request):
    create_footing_form = CreateFootingForm()
    context = {
        'create_footing_form': create_footing_form,
    }
    if request.method == 'POST':
        form = CreateFootingForm(request.POST)
        if form.is_valid():
            data = request.POST.dict()
            data.pop('csrfmiddlewaretoken')
            data.pop('type')

            obj = form.save()
            obj.data = data
            obj.save()

            return redirect('add_rid_view')
    return render(request, 'users_app/create_footing_form.html', context=context)


@user_passes_test(ctt_or_admin_role_check)
def create_contract_view(request):
    create_contract_form = CreateContractsForm()
    context = {
        'create_contract_form': create_contract_form,
    }
    if request.method == 'POST':
        form = CreateContractsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('notifications'))
    return render(request, 'users_app/create_contract_form.html', context=context)


@login_required
def ria_info_view(request, ria_id):
    obj = RIA.objects.get(id=ria_id)

    authors_ria = AuthorsRIA.objects.filter(ria=obj)
    files = DocumentFilesRIA.objects.filter(rid=obj)

    context = {
        'obj_form': ShowRIAForm(instance=obj),
        'obj': obj,
        'authors_ria': authors_ria,
        'files': files,
        'experts': Author.objects.filter(role='expert'),

    }
    try:
        contract = Contracts.objects.get(rid=obj)
        context['contract'] = contract
    except:
        pass
    return render(request, 'users_app/ria_info.html', context=context)


@user_passes_test(ctt_or_admin_role_check)
def submit_for_consideration_view(request, ria_id):
    obj = RIA.objects.get(id=ria_id)
    obj.status = enums.RIAStatus.D

    journal_ = {
        "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "user": request.user.username,
        "action": "РИД передан на рассмотрение сотрудникам ЦТТ"
    }
    obj.journal.append(journal_)

    obj.save()

    information_stage = []
    ctt_workers = Author.objects.filter(role__in=['urist', 'patent', 'manager'])
    for worker in ctt_workers:
        not_data = {
            'user': worker,
            'category': NotificationCategories.RID,
            'text': 'Получен новый РИД на согласование'
        }
        Notifications.objects.create(**not_data)

        temp_data = {
            "expert_id": worker.pk,
            "expertise": "Соответствует роли",
            "count_days": 7,
            'status': 'Получена',
        }
        information_stage.append(temp_data)
    Decision.objects.create(type='a', information_agenda='Согласование Экспертизы ЦТТ по РИД',
                            information_stage=information_stage, ria=obj, status='a')

    return redirect('notifications')


@user_passes_test(ctt_or_admin_role_check)
def set_main_ctt_worker_view(request, ria_id):
    ctt_worker = Author.objects.get(user=request.user)

    obj = RIA.objects.get(id=int(ria_id))
    obj.main_ctt_worker = ctt_worker
    obj.status = enums.RIAStatus.C

    journal_ = {
        "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "user": request.user.username,
        "action": "РИД принят на рассмотрение"
    }
    obj.journal.append(journal_)

    obj.save()

    return redirect('create_decision_type_a_view', ria_id=int(ria_id))


def send_retrieve_request_view(request, ria_id):
    obj = RIA.objects.get(id=int(ria_id))
    obj.status = enums.RIAStatus.F

    not_data = {
        'user': obj.main_ctt_worker,
        'category': NotificationCategories.EXPERTIZE,
        'text': 'Отправлен повторный запрос на рассмотрение'
    }
    Notifications.objects.create(**not_data)

    journal_ = {
        "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "user": request.user.username,
        "action": "Повторно передан на рассмотрение экспертам по экспертизе ЦТТ по РИД"
    }
    obj.journal.append(journal_)
    obj.save()
    information_stage = []
    ctt_workers = Author.objects.filter(role__in=['urist', 'patent', 'manager'])
    for worker in ctt_workers:
        temp_data = {
            "expert_id": worker.pk,
            "expertise": 'Соответствует роли',
            "count_days": 7,
            'status': 'Получена',
        }
        information_stage.append(temp_data)

        not_data = {
            'user': worker,
            'category': NotificationCategories.EXPERTIZE,
            'text': 'Получен новый РИД на согласование'
        }
        Notifications.objects.create(**not_data)

    Decision.objects.create(type='aa', information_agenda='Повторное Согласование Экспертизы ЦТТ по РИД',
                            information_stage=information_stage, ria=obj, status='a')

    return redirect('notifications')


def rid_edit_rospatent_view(request, rid_id):
    rid = RIA.objects.get(id=rid_id)
    form = RidEditRospatentForm(instance=rid)
    if request.POST:
        rospatent = request.POST.get('rospatent')
        rid.rospatent = rospatent
        journal_ = {
            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "user": request.user.username,
            "action": "Внесены данные роспатента"
        }
        rid.journal.append(journal_)
        rid.save()
        return redirect('notifications')
    context = {
        'form': form,
        'obj': rid,
    }
    return render(request, 'users_app/rid_editor.html', context)


def rid_confirm_rospatent_view(request, rid_id):
    rid = RIA.objects.get(id=rid_id)
    rid.status = enums.RIAStatus.M
    journal_ = {
        "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "user": request.user.username,
        "action": "Подтвердил получение охранного документа"
    }
    rid.journal.append(journal_)
    rid.save()
    return redirect('notifications')


def rid_edit_accounting_view(request, rid_id):
    rid = RIA.objects.get(id=rid_id)
    form = RidEditAccountingForm(instance=rid)
    if request.POST:
        accounting = request.POST.get('accounting')
        rid.status = enums.RIAStatus.Q
        rid.accounting = accounting
        rid.save()
        return redirect('notifications')
    context = {
        'form': form,
    }
    return render(request, 'users_app/rid_editor.html', context)


def rid_edit_contract_view(request, rid_id):
    rid = RIA.objects.get(id=rid_id)
    form = RidEditContractsForm(instance=rid)
    free_contracts = Contracts.objects.filter(rid=None)
    if request.POST:
        contract_pk = request.POST.get('contract_pk')
        if contract_pk:
            contract = Contracts.objects.get(pk=contract_pk)
            contract.rid = rid
            contract.save()

            rid.status = enums.RIAStatus.R
            rid.save()
            return redirect('notifications')
    context = {
        'form': form,
        'free_contracts': free_contracts,
    }
    return render(request, 'users_app/rid_editor.html', context)


def rid_edit_contract_payment_view(request, rid_id):
    rid = RIA.objects.get(id=rid_id)
    if request.POST:
        rid.status = enums.RIAStatus.X
        rid.save()
        return redirect('notifications')
    return render(request, 'users_app/rid_editor.html', {})


def rid_edit_view(request, rid_id):
    rid = RIA.objects.get(id=rid_id)
    form = CreateRIAForm(instance=rid)
    if request.POST:
        form = CreateRIAForm(request.POST, instance=rid)
        if form.is_valid():
            obj = form.save()
            journal_ = {
                "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "user": request.user.username,
                "action": "Внес изменения"
            }
            obj.journal.append(journal_)
            obj.save()
        return redirect('notifications')
    context = {
        'form': form,
        'header': 'Редактирование РИД'
    }
    return render(request, 'users_app/rid_editor.html', context)


def get_template_footing_view(request):
    type_ = request.GET.get('type')
    if type_ == 'PLN':
        template = 'users_app/footing_type_pln.html'
    elif type_ == 'QST':
        template = 'users_app/footing_type_qst.html'
    elif type_ == 'OTH':
        template = 'users_app/footing_type_oth.html'
    else:
        template = 'users_app/footing_type_cnt.html'
    html = render_to_string(template, {})
    return HttpResponse(html)


def author_detail_view(request, pk):
    obj = get_object_or_404(Author, pk=pk)
    form = AuthorDetailForm(instance=obj)
    context = {
        'page_name': "Информация об авторе",
        'form': form,
        'obj': obj,
    }
    return render(request, 'users_app/author_detail.html', context)


@user_passes_test(ctt_or_admin_role_check)
def author_edit_view(request, pk):
    obj = get_object_or_404(Author, pk=pk)
    form = AuthorEditForm(instance=obj)
    context = {
        'page_name': "Изменить информацию об авторе",
        'form': form,
    }
    if request.POST:
        form = AuthorEditForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
        return redirect('author_detail', pk=pk)

    return render(request, 'users_app/author_edit.html', context)


class RIAList(APIView):

    def get(self, request):
        rias = RIA.objects.all()
        data = {
            "total": rias.count(),
            "totalNotFiltered": rias.count(),
        }
        rows = []
        for ria in rias:
            temp_ = {
                'name': self.get_link_name(ria),
                'authors': self.get_authors(ria),
                'division': ria.get_division_display(),
                'main_ctt_worker': self.get_main_ctt_worker_link(ria),
                'status': ria.get_status_display(),
            }
            rows.append(temp_)
        data['rows'] = rows
        return Response(data)

    def get_authors(self, ria):
        authors_ria = AuthorsRIA.objects.filter(ria=ria)
        names = []
        for author_ria in authors_ria:
            name = author_ria.author.name
            lazy = reverse_lazy('author_detail', args=(author_ria.author.pk,))
            html_ = format_html("<a href='{}'>{}</a>", lazy, name)
            names.append(html_)
        text = '<br>'.join(names)
        return format_html(text)

    def get_link_name(self, ria):
        lazy = reverse_lazy('ria_info_view', args=(ria.pk,))
        html_ = format_html("<a href='{}'>{}</a>", lazy, ria.name)
        return html_

    def get_main_ctt_worker_link(self, ria):
        if ria.main_ctt_worker:
            lazy = reverse_lazy('author_detail', args=(ria.main_ctt_worker.pk,))
            html_ = format_html("<a href='{}'>{}</a>", lazy, ria.main_ctt_worker.name)
            return html_
        else:
            return None


def footing_info_view(request, pk):
    obj = get_object_or_404(Footing, pk=pk)
    form = FootingDetailForm(instance=obj)
    data = obj.data
    context = {
        'page_name': "Информация о учете оснований для создания РИД",
        'obj': obj,
        'form': form,
        'data': data,
    }
    return render(request, 'users_app/footing_detail.html', context)


def contract_info_view(request, pk):
    obj = get_object_or_404(Contracts, pk=pk)
    form = ContractsDetailForm(instance=obj)
    context = {
        'page_name': "Информация о договоре",
        'obj': obj,
        'form': form,
    }
    return render(request, 'users_app/contract_detail.html', context)


@login_required
def contract_reestr_view(request):
    context = {
        'active_button': 'contract_reestr',
    }
    return render(request, 'users_app/contract_reestr.html', context)


class ContractList(APIView):
    def get(self, request):
        contracts = Contracts.objects.all()
        data = {
            "total": contracts.count(),
            "totalNotFiltered": contracts.count(),
        }
        rows = []
        for contract in contracts:
            temp_ = {
                'holder': contract.holder,
                'recipient': contract.recipient,
                'number': self.get_link_name(contract),
                'date': contract.date,
                'period': contract.period,
                'rid': self.get_link_ria(contract.rid) if contract.rid else '-'
            }
            rows.append(temp_)
        data['rows'] = rows
        return Response(data)

    def get_link_name(self, contract):
        lazy = reverse_lazy('contract_info', args=(contract.pk,))
        html_ = format_html("<a href='{}'>{}</a>", lazy, contract.number)
        return html_

    def get_link_ria(self, ria):
        lazy = reverse_lazy('ria_info_view', args=(ria.pk,))
        html_ = format_html("<a href='{}'>{}</a>", lazy, ria.name)
        return html_


class DecisionList(APIView):
    def get(self, request):
        decisions = Decision.objects.all()
        data = {
            "total": decisions.count(),
            "totalNotFiltered": decisions.count(),
        }
        rows = []
        for decision in decisions:
            temp_ = {
                'agenda': self.get_link_agenda(decision),
                'type': decision.get_type_display(),
                'rid': self.get_link_ria(decision.ria),
                'status': decision.get_status_display(),
            }
            rows.append(temp_)
        data['rows'] = rows
        return Response(data)

    def get_link_agenda(self, decision):
        lazy = reverse_lazy('exp_info_view', args=(decision.pk,))
        html_ = format_html("<a href='{}'>{}</a>", lazy, decision.information_agenda)
        return html_

    def get_link_ria(self, ria):
        lazy = reverse_lazy('ria_info_view', args=(ria.pk,))
        html_ = format_html("<a href='{}'>{}</a>", lazy, ria.name)
        return html_


def contract_edit_view(request, pk):
    obj = get_object_or_404(Contracts, pk=pk)
    form = ContractsEditForm(instance=obj)
    if request.POST:
        form = ContractsEditForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('notifications')
    context = {
        'page_name': "Редактирование договора",
        'obj': obj,
        'form': form,
    }
    return render(request, 'users_app/contract_edit.html', context)


from django.db.models import Q


def statistic_view(request):
    statistic = {
        'Количество РИД на согласовании в ЦТТ': RIA.objects.filter(
            Q(status=enums.RIAStatus.D) | Q(status=enums.RIAStatus.G)).count(),
        'Количество РИД на комиссии ИС по принятию решения о необходимости правовой охраны': RIA.objects.filter(
            status=enums.RIAStatus.J).count(),
        'Количество РИД, по которым получен правоохранный документ': RIA.objects.filter(
            status=enums.RIAStatus.M).count(),
        'Количество РИД, по которым отказано в правоохранном документе': RIA.objects.filter(
            status=enums.RIAStatus.K).count(),
        'Количество РИД, по которым заключены лицензионные договоры': RIA.objects.filter(
            status=enums.RIAStatus.R).count(),

        'Количество согласований на рассмотрении': Decision.objects.filter(status='a').count(),
        'Количество согласований, по которым принято положительное решение': Decision.objects.filter(
            status='c').count(),
        'Количество согласований, по которым принято отрицательное решение': Decision.objects.filter(
            status='d').count(),
    }
    context = {
        'statistic_list': statistic,
        'page_name': 'Статистика',
        'active_button': 'statistic'
    }
    return render(request, 'users_app/statistic.html', context=context)


from django.db.models import Count


# ◦ Динамика создания РИД, по годам, по видам РИД (количество)
# ◦ Динамика получения правоохранных документов, по годам , по видам РИД (количество)
# ◦ Динамика заключения договоров использования, по годам, по типам договоров (количество)
# ◦ Динамика конвертации по годам: уведомления в заявку, заявка в патент, патент в сделку (договор). По годам, по видам РИД (количество)
def dashboards_view(request):
    dcr_type_categories = enums.TypeRIA.choices
    dcr_type_data = [RIA.objects.filter(type=temp_type[0]).aggregate(total=Count('id')).get('total') for temp_type in
                     dcr_type_categories]

    dc_type_categories = enums.TypeRIA.choices
    ntp_data = [RIA.objects.filter(type=temp_type[0], status__in=['H']).aggregate(total=Count('id')).get('total') for
                temp_type in dcr_type_categories]
    ptp_data = [RIA.objects.filter(type=temp_type[0], status__in=['M']).aggregate(total=Count('id')).get('total') for
                temp_type in dcr_type_categories]
    ptd_data = [RIA.objects.filter(type=temp_type[0], status__in=['R']).aggregate(total=Count('id')).get('total') for
                temp_type in dcr_type_categories]

    context = {
        'active_button': 'dashboards',
        'dcr_type_categories': dcr_type_categories,
        'dcr_type_data': dcr_type_data,

        'dc_type_categories': dc_type_categories,
        'ntp_data': ntp_data,
        'ptp_data': ptp_data,
        'ptd_data': ptd_data,
    }
    return render(request, 'users_app/dashboards.html', context=context)

