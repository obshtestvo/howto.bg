from forum.settings.base import Setting, SettingSet
from django.utils.translation import ugettext_lazy as _

LDAP_SET = SettingSet('ldap', _('LDAP settings'), _("LDAP configuration for OSQA"), 4)

LDAP_SERVER = Setting('LDAP_SERVER', '', LDAP_SET, dict(
label = _("LDAP Server"),
help_text = _("The hostname of your organization's LDAP server"),
required = False))

LDAP_USE_TLS = Setting('LDAP_USE_TLS', False, LDAP_SET, dict(
label = _("Use TLS"),
help_text = _("Check to use TLS"),
required = False))

LDAP_BIND_DN = Setting('LDAP_BIND_DN', '', LDAP_SET, dict(
label = _("DN for binding"),
help_text = _("Enter the DN to use to bind to the LDAP server (leave blank for anonymous bind)"),
required = False))

LDAP_BIND_SECRET = Setting('LDAP_BIND_SECRET', '', LDAP_SET, dict(
label = _("Password for binding"),
help_text = _("Password for binding DN above"),
required = False))

LDAP_BASE_DN = Setting('LDAP_BASE_DN', '', LDAP_SET, dict(
label = _("Base DN"),
help_text = _("The Base DN used to search for users"),
required = False))

LDAP_USER_MASK = Setting('LDAP_USER_MASK', 'UID=%s', LDAP_SET, dict(
label = _("User Mask"),
help_text = _("The mask to query for a User"),
required = False))

LDAP_UID = Setting('LDAP_UID', 'uid', LDAP_SET, dict(
label = _("uid field"),
help_text = _("ldap field that holds the uid (sAMAccountName in AD)"),
required = False))

LDAP_NAME = Setting('LDAP_NAME', 'cn', LDAP_SET, dict(
label = _("Name field"),
help_text = _("ldap field that holds the full name (displayName in AD)"),
required = False))

LDAP_DN = Setting('LDAP_DN', 'dn', LDAP_SET, dict(
label = _("DN field"),
help_text = _("ldap field that holds the distinguished name (distinguishedName in AD)"),
required = False))

LDAP_MAIL = Setting('LDAP_MAIL', 'mail', LDAP_SET, dict(
label = _("email field"),
help_text = _("ldap field that holds the email"),
required = False))
