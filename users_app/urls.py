from django.urls import path
from users_app.views.other_views import *
from users_app.views.decision_views import *
from users_app.views.reestr_views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('registration/', registration_view, name='registration'),
    path('auth/', user_auth_view, name='user_auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', account_view, name='account'),
    path('create_ria/', add_rid_view, name='add_rid_view'),
    path('notifications/', notifications, name='notifications'),
    path('create_footing/', create_footing_view, name='create_footing_view'),
    path('create_contract/', create_contract_view, name='create_contract_view'),
    path('create_decision/', create_decision_view, name='create_decision_view'),
    path('ria_info/<int:ria_id>', ria_info_view, name='ria_info_view'),
    path('set_main_ctt_worker/<int:ria_id>', set_main_ctt_worker_view, name='set_main_ctt_worker_view'),
    path('submit_for_consideration/<int:ria_id>/', submit_for_consideration_view, name='submit_for_consideration'),
    path('send_retrieve_request/<int:ria_id>/', send_retrieve_request_view, name='send_retrieve_request'),

    path('create_decision_type_a/<int:ria_id>/', create_decision_type_a_view, name='create_decision_type_a_view'),
    path('create_decision_type_a_onemore_view/<int:ria_id>/', create_decision_type_a_onemore_view,
         name='create_decision_type_a_onemore_view'),
    path('create_decision_type_b/<int:ria_id>/', create_decision_type_b_view, name='create_decision_type_b_view'),
    path('create_decision_type_c/<int:ria_id>/', create_decision_type_c_view, name='create_decision_type_c_view'),
    path('create_decision_type_g/<int:ria_id>/', create_decision_type_g_view, name='create_decision_type_g_view'),

    path('create_author/', create_author_view, name='create_author'),
    path('author_info/<pk>', author_detail_view, name='author_detail'),
    path('author_edit/<pk>', author_edit_view, name='author_edit'),

    path('contract_info/<pk>', contract_info_view, name='contract_info'),
    path('contract_edit/<pk>', contract_edit_view, name='contract_edit'),
    path('contract_reestr/', contract_reestr_view, name='contract_reestr'),

    path('footint_info/<pk>', footing_info_view, name='footing_info'),

    path('my_expertise/', my_decision_view, name='my_expertise_view'),
    path('update_status_exp/', update_status_exp_view, name='update_status_exp_view'),
    path('active_expertise/', active_decision_view, name='active_expertise_view'),
    path('exp_info/<int:exp_id>/', decision_info_view, name='exp_info_view'),

    path('update_status_decision_view/<int:decision_id>', update_status_decision_view,
         name='update_status_decision_view'),
    path('update_status_decision_type_a_onemore_view/<int:decision_id>', update_status_decision_type_a_onemore_view,
         name='update_status_decision_type_a_onemore_view'),
    path('update_status_decision_type_b_view/<int:decision_id>', update_status_decision_type_b_view,
         name='update_status_decision_type_b_view'),
    path('update_status_decision_type_c_view/<int:decision_id>', update_status_decision_type_c_view,
         name='update_status_decision_type_c_view'),
    path('update_status_decision_type_g_view/<int:decision_id>', update_status_decision_type_g_view,
         name='update_status_decision_type_g_view'),

    path('rid_edit/<int:rid_id>', rid_edit_view, name='rid_edit'),
    path('rid_edit_rospatent/<int:rid_id>/', rid_edit_rospatent_view, name='rid_edit_rospatent_view'),
    path('rid_confirm_rospatent/<int:rid_id>/', rid_confirm_rospatent_view, name='rid_confirm_rospatent_view'),
    path('rid_edit_accounting/<int:rid_id>/', rid_edit_accounting_view, name='rid_edit_accounting_view'),
    path('rid_edit_contract/<int:rid_id>/', rid_edit_contract_view, name='rid_edit_contract_view'),
    path('rid_edit_contract_payment/<int:rid_id>/', rid_edit_contract_payment_view,
         name='rid_edit_contract_payment_view'),

    path('get_template_footing/', get_template_footing_view, name='get_template_footing'),

    path('statistic/', statistic_view, name='statistic'),
    path('dashboards/', dashboards_view, name='dashboards'),

    path('get_ria_data_table/', RIAList.as_view(), name='get_ria_data_table'),
    path('get_contract_data_table/', ContractList.as_view(), name='get_contract_data_table'),
    path('get_decision_data_table/', DecisionList.as_view(), name='get_decision_data_table'),
    path('get_reestr_data_table/', ReestrList.as_view(), name='get_reestr_data_table'),

    # reestr views
    path('reestr/', ReestrView.as_view(), name='reestr'),
    path('reestr/<pk>/', ReestrDetailView.as_view(), name='reestr-detail'),
    path('reestr/update/<pk>/', ReestrUpdateView.as_view(), name='reestr-update')
]
