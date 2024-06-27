from .models import Notifications, Author


def notifications(request):
    if request.user.is_authenticated:
        try:
            user = Author.objects.get(user=request.user)
            notifications_ = Notifications.objects.filter(user=user).order_by('-datetime_create')
        except:
           notifications_ = None 
    else:
        notifications_ = None
    return {'notifications': notifications_}


def my_role(request):
    if request.user.is_authenticated:
        try:
            user = Author.objects.get(user=request.user)
            role = user.role
        except:
            role = None
    else:
        role = None
    return {'my_role': role}
