"""
Context processor for lightweight session messages.

Time-stamp: <2008-07-19 23:16:19 carljm context_processors.py>

"""
from django.utils.encoding import StrAndUnicode

from django.contrib.messages.api import get_messages

def user_messages (request):
    """
    Returns session messages for the current session.

    """
    return { 'user_messages': get_messages(request) }
