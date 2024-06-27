from .models import *


def ctt_role_check(user):
    role = Author.objects.get(user=user).role
    if role == 'ctt':
        return True
    else:
        return False


def ctt_or_admin_role_check(user):
    role = Author.objects.get(user=user).role
    if role == 'ctt' or role == 'admin':
        return True
    else:
        return False
