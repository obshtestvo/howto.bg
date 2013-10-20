from forum.authentication.base import AuthenticationConsumer, ConsumerTemplateContext, InvalidAuthentication
from forum.models import User
from forum.actions import UserJoinsAction
from django.utils.translation import ugettext as _
from forum import settings

class LDAPAuthConsumer(AuthenticationConsumer):

    def process_authentication_request(self, request):
        username = request.POST['username'].strip()
        password = request.POST['password']
        uid = str(settings.LDAP_USER_MASK) % username

        #an empty password will cause ldap to try an anonymous bind. This is picked up here
        if not password:
            raise InvalidAuthentication(_('Login failed. Please enter valid username and password (both are case-sensitive)'))

        ldapo = ldap.initialize(str(settings.LDAP_SERVER))
        if(settings.LDAP_USE_TLS):
            ldapo.start_tls_s()
        ldapo.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        try:
            ldapo.simple_bind_s(str(settings.LDAP_BIND_DN), str(settings.LDAP_BIND_SECRET))
            search = ldapo.search_s(str(settings.LDAP_BASE_DN), ldap.SCOPE_SUBTREE, uid)
        except ldap.LDAPError:
            #could not bind using credentials specified in ldap config
            raise InvalidAuthentication(_('Login failed - LDAP bind error. Please contact your system administrator'))

        ldapo.unbind_s()

        if not search:
            #could not find user
            raise InvalidAuthentication(_('Login failed. Please enter valid username and password (both are case-sensitive)'))

        #now try to bind as selected user; should raise exception if bind fails
        ldapo = ldap.initialize(str(settings.LDAP_SERVER))
        if(settings.LDAP_USE_TLS):
            ldapo.start_tls_s()
        ldapo.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        try:
            ldapo.simple_bind_s(search[0][1][str(settings.LDAP_DN)][0],password)
        except ldap.LDAPError:
            #could not bind as user - password is incorrect
            raise InvalidAuthentication(_('Login failed. Please enter valid username and password (both are case-sensitive)'))
        ldapo.unbind_s()

        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            userinfo = search[0][1]
            _user = User( username = userinfo[str(settings.LDAP_UID)][0],
                          email = userinfo[str(settings.LDAP_MAIL)][0],
                          real_name = userinfo[str(settings.LDAP_NAME)][0] )
            _user.email_isvalid = True
            _user.set_unusable_password()
            _user.save()
            UserJoinsAction(user=_user, ip=request.META['REMOTE_ADDR']).save()
            return _user

class LDAPAuthContext(ConsumerTemplateContext):
    mode = 'STACK_ITEM'
    weight = 1000
    human_name = 'LDAP authentication'
    stack_item_template = 'modules/ldapauth/loginform.html'
    show_to_logged_in_user = False
