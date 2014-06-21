from forum import settings

def application_settings(context):
    return {'settings': settings}

def auth_processor(request):
    if hasattr(request, 'user'):
        user = request.user
    else:
        from django.contrib.auth.models import AnonymousUser
        user = AnonymousUser()

    from django.core.context_processors import PermWrapper
    return {
        'user': user,
        'perms': PermWrapper(user),
    }
