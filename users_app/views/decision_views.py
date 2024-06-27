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

@user_passes_test(ctt_or_admin_role_check)
def create_decision_view(request):
    create_decision_from = CreateDecisionForm()
    context = {
        'create_decision_from': create_decision_from,
    }
    if request.method == 'POST':
        form = CreateDecisionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('add_rid_view'))
    return render(request, 'users_app/create_decision_from.html', context=context)

@user_passes_test(ctt_or_admin_role_check)
def create_decision_type_a_view(request, ria_id):
    context = {
        'experts': Author.objects.filter(role='expert'),
        'ria_id': ria_id,
    }
    if request.POST:
        ria_obj = RIA.objects.get(id=int(ria_id))
        ria_obj.status = enums.RIAStatus.D
        journal_ = {
            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "user": request.user.username,
            "action": "Передан на рассмотрение экспертам по экспертизе ЦТТ по РИД"
        }
        ria_obj.journal.append(journal_)
        ria_obj.save()
        information_stage = []
        for expert_id, expertise, count_days in zip(request.POST.getlist('expert_id'),
                                                    request.POST.getlist('expertise'),
                                                    request.POST.getlist('count_days')):
            temp_data = {
                "expert_id": expert_id,
                "expertise": expertise,
                "count_days": count_days,
                'status': 'Получена',
            }
            information_stage.append(temp_data)
        Decision.objects.create(type='a', information_agenda='Согласование Экспертизы ЦТТ по РИД',
                                information_stage=information_stage, ria=ria_obj, status='a')
        for expert_id in request.POST.getlist('expert_id'):
            not_data = {
                'user': Author.objects.get(id=int(expert_id)),
                'category': NotificationCategories.EXPERTIZE,
                'text': 'Получен новый РИД на согласование'
            }
            Notifications.objects.create(**not_data)
        return redirect('notifications')
    return render(request, 'users_app/create_decision_type_a.html', context)


@user_passes_test(ctt_or_admin_role_check)
def create_decision_type_a_onemore_view(request, ria_id):
    context = {
        'experts': Author.objects.filter(role='expert'),
        'ria_id': ria_id,
    }
    if request.POST:
        ria_obj = RIA.objects.get(id=int(ria_id))
        ria_obj.status = enums.RIAStatus.G
        journal_ = {
            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "user": request.user.username,
            "action": "Повторно передан на рассмотрение экспертам по экспертизе ЦТТ по РИД"
        }
        ria_obj.journal.append(journal_)
        ria_obj.save()
        information_stage = []
        for expert_id, expertise, count_days in zip(request.POST.getlist('expert_id'),
                                                    request.POST.getlist('expertise'),
                                                    request.POST.getlist('count_days')):
            temp_data = {
                "expert_id": expert_id,
                "expertise": expertise,
                "count_days": count_days,
                'status': 'Получена',
            }
            information_stage.append(temp_data)
        Decision.objects.create(type='aa', information_agenda='Повторное Согласование Экспертизы ЦТТ по РИД',
                                information_stage=information_stage, ria=ria_obj, status='a')
        for expert_id in request.POST.getlist('expert_id'):
            not_data = {
                'user': Author.objects.get(id=int(expert_id)),
                'category': NotificationCategories.EXPERTIZE,
                'text': 'Получен новый РИД на согласование'
            }
            Notifications.objects.create(**not_data)
        return redirect('notifications')
    return render(request, 'users_app/create_decision_type_a_onemore.html', context)


@user_passes_test(ctt_or_admin_role_check)
def create_decision_type_b_view(request, ria_id):
    context = {
        'experts': Author.objects.filter(role='expert'),
        'ria_id': ria_id,
    }
    if request.POST:
        ria_obj = RIA.objects.get(id=int(ria_id))
        journal_ = {
            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "user": request.user.username,
            "action": "Передан на рассмотрение экспертам по экспертизу о необходимости правовой охраны РИД"
        }
        ria_obj.journal.append(journal_)
        ria_obj.status = enums.RIAStatus.J
        ria_obj.save()
        information_stage = []
        for expert_id, expertise, count_days in zip(request.POST.getlist('expert_id'),
                                                    request.POST.getlist('expertise'),
                                                    request.POST.getlist('count_days')):
            temp_data = {
                "expert_id": expert_id,
                "expertise": expertise,
                "count_days": count_days,
                'status': 'Получена',
            }
            information_stage.append(temp_data)
        Decision.objects.create(type='b', information_agenda='Согласование решения о необходимости правовой охраны РИД',
                                information_stage=information_stage, ria=ria_obj, status='a')
        for expert_id in request.POST.getlist('expert_id'):
            not_data = {
                'user': Author.objects.get(id=int(expert_id)),
                'category': NotificationCategories.EXPERTIZE,
                'text': 'Получен новый РИД на согласование'
            }
            Notifications.objects.create(**not_data)
        return redirect('active_expertise_view')
    return render(request, 'users_app/create_decision_type_b.html', context)


def create_decision_type_c_view(request, ria_id):
    context = {
        'experts': Author.objects.filter(role='expert'),
        'ria_id': ria_id,
    }
    if request.POST:
        ria_obj = RIA.objects.get(id=int(ria_id))
        journal_ = {
            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "user": request.user.username,
            "action": "Передан на рассмотрение экспертам по Решения Комиссии НМА"
        }
        ria_obj.journal.append(journal_)
        ria_obj.status = enums.RIAStatus.N
        ria_obj.save()
        information_stage = []
        for expert_id, expertise, count_days in zip(request.POST.getlist('expert_id'),
                                                    request.POST.getlist('expertise'),
                                                    request.POST.getlist('count_days')):
            temp_data = {
                "expert_id": expert_id,
                "expertise": expertise,
                "count_days": count_days,
                'status': 'Получена',
            }
            information_stage.append(temp_data)
        Decision.objects.create(type='c', information_agenda='Согласование Решения Комиссии НМА',
                                information_stage=information_stage, ria=ria_obj, status='a')
        for expert_id in request.POST.getlist('expert_id'):
            not_data = {
                'user': Author.objects.get(id=int(expert_id)),
                'category': NotificationCategories.EXPERTIZE,
                'text': 'Получен новый РИД на согласование'
            }
            Notifications.objects.create(**not_data)
        return redirect('active_expertise_view')
    return render(request, 'users_app/create_decision_type_c.html', context)


def create_decision_type_g_view(request, ria_id):
    context = {
        'experts': Author.objects.filter(role='expert'),
        'ria_id': ria_id,
    }
    if request.POST:
        ria_obj = RIA.objects.get(id=int(ria_id))
        journal_ = {
            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "user": request.user.username,
            "action": "Передан на рассмотрение экспертам по Согласование договора распоряжения правом"
        }
        ria_obj.journal.append(journal_)
        ria_obj.status = enums.RIAStatus.S
        ria_obj.save()
        information_stage = []
        for expert_id, expertise, count_days in zip(request.POST.getlist('expert_id'),
                                                    request.POST.getlist('expertise'),
                                                    request.POST.getlist('count_days')):
            temp_data = {
                "expert_id": expert_id,
                "expertise": expertise,
                "count_days": count_days,
                'status': 'Получена',
            }
            information_stage.append(temp_data)
        Decision.objects.create(type='g', information_agenda='Рассмотрение сведений по договору',
                                information_stage=information_stage, ria=ria_obj, status='a')
        for expert_id in request.POST.getlist('expert_id'):
            not_data = {
                'user': Author.objects.get(id=int(expert_id)),
                'category': NotificationCategories.EXPERTIZE,
                'text': 'Получен новый РИД на согласование'
            }
            Notifications.objects.create(**not_data)
        return redirect('active_expertise_view')
    return render(request, 'users_app/create_decision_type_g.html', context)

def update_status_decision_view(request):
    if request.POST:
        expid = int(request.POST['expid'])
        expertise = request.POST['expertise']
        status = request.POST['status']
        decision = Decision.objects.get(id=expid)
        information_stage = exp.information_stage
        for stage in information_stage:
            if expertise == stage['expertise']:
                stage['status'] = status

        all_statuses = [stage['status'] for stage in information_stage]
        if all([status in ['Принята', 'Отклонена'] for status in all_statuses]):
            decision.status = 'b'

        ria_obj = exp.ria
        journal_ = {
            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "user": request.user.username,
            "action": f"Выполнил действие {status} для экспертизы {expertise}"
        }
        ria_obj.journal.append(journal_)
        ria_obj.save()

        decision.save()
        return redirect('my_expertise_view')

    return redirect('my_expertise_view')

def my_decision_view(request):
    my_id = Author.objects.get(user=request.user).id
    data = []
    for exp in Decision.objects.all():
        information_stage = exp.information_stage
        exp_ids = [int(stage['expert_id']) for stage in information_stage]
        if my_id in exp_ids:
            for stage in information_stage:
                if my_id == int(stage['expert_id']):
                    temp_data = {
                        'exp_id': exp.id,
                        'ria_id': exp.ria.id,
                        'expertise': stage['expertise'],
                        'count_days': stage['count_days'],
                        'status': stage.get('status', None)
                    }
                    data.append(temp_data)
    context = {
        'active_button': 'my_expertise_view',
        'data': data
    }
    return render(request, 'users_app/my_exp.html', context)

@user_passes_test(ctt_or_admin_role_check)
def active_decision_view(request):
    user = Author.objects.get(user=request.user)
    rias = RIA.objects.filter(main_ctt_worker=user)
    decisions = Decision.objects.filter(ria__in=rias)

    context = {
        'active_button': 'active_expertise_view',
        'table': ActiveExpertiseTable(decisions)
    }
    return render(request, 'users_app/active_expertise.html', context)



@user_passes_test(ctt_or_admin_role_check)
def decision_info_view(request, exp_id):
    decision = Decision.objects.get(id=exp_id)
    information_stage = decision.information_stage
    data = []
    for stage in information_stage:
        temp_data = {
            'expert': Author.objects.get(id=int(stage['expert_id'])).name,
            'expertise': stage['expertise'],
            'count_days': stage['count_days'],
            'status': stage.get('status', None)
        }
        data.append(temp_data)
    context = {
        'obj': decision,
        'obj_type': decision.get_type_display(),
        'data': data,
        'experts': Author.objects.filter(role='expert'),
    }
    if decision.type == 'a':
        return render(request, 'users_app/exp_info.html', context)
    elif decision.type == 'aa':
        return render(request, 'users_app/exp_info_type_a_onemore.html', context)
    elif decision.type == 'b':
        return render(request, 'users_app/exp_info_type_b.html', context)
    elif decision.type == 'c':
        return render(request, 'users_app/exp_info_type_c.html', context)
    elif decision.type == 'g':
        return render(request, 'users_app/exp_info_type_g.html', context)


def update_status_decision_view(request, decision_id):
    decision = Decision.objects.get(id=decision_id)
    ria = decision.ria
    status = request.POST['status']
    if status == 'Принята':
        decision_status = enums.RIAStatus.H
        ria.status = decision_status

        journal_ = {
            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "user": request.user.username,
            "action": f"Принял проверка ЦТТ по РИД"
        }
        ria.journal.append(journal_)
        ria.save()

        decision.status = 'c'
        decision.save()

        return JsonResponse({'redirect': reverse_lazy('create_decision_type_b_view', args=(decision.ria.id,))})
    else:
        decision_status = enums.RIAStatus.E
        ria.status = decision_status
        ria.save()
        user = decision.ria.main_ctt_worker
        not_data = {
            'user': user,
            'category': NotificationCategories.EXPERTIZE,
            'text': 'РИД не прошел проверку ЦТТ по РИД. РИД отправлен на доработку.'
        }
        Notifications.objects.create(**not_data)

        decision.status = 'd'
        decision.save()
        return JsonResponse({'redirect': reverse_lazy('notifications')})

    return redirect('active_expertise_view')


def update_status_decision_type_a_onemore_view(request, decision_id):
    decision = Decision.objects.get(id=decision_id)
    ria = decision.ria
    status = request.POST['status']
    if status == 'Принята':
        decision_status = enums.RIAStatus.H
        ria.status = decision_status

        journal_ = {
            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "user": request.user.username,
            "action": f"Принял проверка ЦТТ по РИД"
        }
        ria.journal.append(journal_)
        ria.save()

        decision.status = 'c'
        decision.save()

        return JsonResponse({'redirect': reverse_lazy('create_decision_type_b_view', args=(decision.ria.id,))})
    else:
        decision_status = enums.RIAStatus.I
        ria.status = decision_status
        ria.save()
        user = decision.ria.main_ctt_worker
        not_data = {
            'user': user,
            'category': NotificationCategories.EXPERTIZE,
            'text': 'РИД не прошел повторную проверку ЦТТ по РИД'
        }
        Notifications.objects.create(**not_data)

        decision.status = 'd'
        decision.save()
        return JsonResponse({'redirect': reverse_lazy('notifications')})

    return redirect('active_expertise_view')



def update_status_decision_type_b_view(request, decision_id):
    decision = Decision.objects.get(id=decision_id)
    status = request.POST['status']
    if status == 'Принята':
        rid_status = enums.RIAStatus.L
        action_status = 'Одобрил необходимость правовой охраны'
        decision.status ='c'

    else:
        decision.status ='d'
        rid_status = enums.RIAStatus.K
        action_status = 'Отклонил РИД'
        user = decision.ria.main_ctt_worker
        not_data = {
            'user': user,
            'category': NotificationCategories.EXPERTIZE,
            'text': 'РИД не принят'
        }
        Notifications.objects.create(**not_data)

    rid = decision.ria
    rid.status = rid_status
    journal_ = {
        "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "user": request.user.username,
        "action": action_status
    }
    rid.journal.append(journal_)
    rid.save()
    
    decision.save()
    return JsonResponse({'redirect': reverse_lazy('notifications')})


def update_status_decision_type_c_view(request, decision_id):
    decision = Decision.objects.get(id=decision_id)
    status = request.POST['status']
    if status == 'Принята':
        rid_status = enums.RIAStatus.P
        decision.status ='c'

    else:
        decision.status ='d'
        rid_status = enums.RIAStatus.O
        user = decision.ria.main_ctt_worker
        not_data = {
            'user': user,
            'category': NotificationCategories.EXPERTIZE,
            'text': 'РИД не принят'
        }
        Notifications.objects.create(**not_data)
    rid = decision.ria
    rid.status = rid_status
    journal_ = {
        "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "user": request.user.username,
        "action": rid_status
    }
    rid.journal.append(journal_)
    rid.save()
    decision.save()
    return JsonResponse({'redirect': reverse_lazy('notifications')})


def update_status_decision_type_g_view(request, decision_id):
    decision = Decision.objects.get(id=decision_id)
    status = request.POST['status']
    if status == 'Принята':
        decision.status ='c'
        rid_status = enums.RIAStatus.U
    else:
        rid_status = enums.RIAStatus.T
        decision.status ='d'
        user = decision.ria.main_ctt_worker
        not_data = {
            'user': user,
            'category': NotificationCategories.EXPERTIZE,
            'text': 'РИД не принят'
        }
        Notifications.objects.create(**not_data)
    rid = decision.ria
    rid.status = rid_status
    journal_ = {
        "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "user": request.user.username,
        "action": rid_status
    }
    rid.journal.append(journal_)
    rid.save()
    decision.save()
    return JsonResponse({'redirect': reverse_lazy('notifications')})

def update_status_exp_view(request):
    if request.POST:
        expid = int(request.POST['expid'])
        expertise = request.POST['expertise']
        status = request.POST['status']
        exp = Decision.objects.get(id=expid)
        information_stage = exp.information_stage
        for stage in information_stage:
            if expertise == stage['expertise']:
                stage['status'] = status

        all_statuses = [stage['status'] for stage in information_stage]
        if all([status in ['Принята', 'Отклонена'] for status in all_statuses]):
            exp.status = 'Все эксперты приняли решения'

        ria_obj = exp.ria
        journal_ = {
            "time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "user": request.user.username,
            "action": f"Выполнил действие {status} для экспертизы {expertise}"
        }
        ria_obj.journal.append(journal_)
        ria_obj.save()

        exp.save()
        return redirect('my_expertise_view')

    return redirect('my_expertise_view')
