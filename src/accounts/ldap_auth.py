# -*- coding: utf-8 -*-
# SB HBRS
from accounts.models import User
from configuration import get_settings
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import check_password
from django.conf import settings
import ldap

try:
    from settings import LDAP_GROUP_ADAPTERS
except:
    LDAP_GROUP_ADAPTERS = ()

# LDAP-Group-Adapter einmalig "zusammenstellen"
_ldap_group_adapters = []
for a in LDAP_GROUP_ADAPTERS:
    lga = __import__(a)
    _ldap_group_adapters.append(lga.ldap_group_adapter.ldap_group_adapter)

class LDAPBackend:
    """
    Authenticate against our LDAP Database
    """
    def authenticate(self, request, username=None, password=None):
        # alle Usernamen werden klein geschrieben!
        if username:
            username = username.lower()
        # lokaler User vorhanden?
        try:
            localuser = User.objects.get(username=username)
        except User.DoesNotExist:
            localuser = None
        # Wenn bei einem bereits vorhandenen lokalen User keine
        # LDAP-Authentifizierung eingetragen ist, sind wir nicht zuständig.
        if localuser and localuser.password != 'LDAP_AUTH':
            return None
        # LDAP-Abfrage
        ldapUser = fetch_ldapuser_dict(uid=username, password=password)
        # Abbruch, wenn kein entsprechender LDAP-User existiert oder
        # falsches Passwort eingegeben wurde
        if not ldapUser or not ldapUser['password_ok']:
            return None
        if localuser:
            # aktuelle Userdaten aus LDAP uebernehmen
            localuser.email = ldapUser['mail']
            localuser.first_name = _select_attribute([ldapUser['firstName'],
                                                      ldapUser['givenName']])
            localuser.last_name = _select_attribute([ldapUser['lastName'],
                                                     ldapUser['sn']])
            localuser.save()
        else:
            if not get_settings().new_users_via_sso:
                return None
            # Auto create local user on first login
            localuser = create_localuser_from_ldapuser(username, ldapUser)
        # LDAP-Group-Adapter aufrufen
        for lga in _ldap_group_adapters:
            lga(localuser)
        # User, die noch in keiner Grupe sind, in die Gruppe "User" aufnehmen
        if localuser.groups.count() == 0:
            g = Group.objects.get(name='User')
            localuser.groups.add(g)
        return localuser

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def _select_attribute(l):
    # Remove empty strings
    valid_names = filter(lambda name: bool(name), l)
    
    # Select shortest entry due to umlauts
    x = ''
    for y in valid_names:
        if not x or len(y) < len(x):
            x = y
    return x

def fetch_ldapuser_dict(uid, password=None):
    c = ldap.initialize(settings.LDAP_URI)
    # search distinguished name
    filter = 'uid=%s' % uid
    attrlist = ['dn', 'mail', 'firstName', 'lastName', 'displayName', \
                'personalTitle', 'uniqueIdentifier', 'givenName', 'sn']
    results = c.search_st(settings.LDAP_BASE, ldap.SCOPE_SUBTREE, filter, \
                          attrlist, timeout=5)
    if len(results) != 1:
        # no unique entry found
        c.unbind()
        return None
    # prepare results
    dn = results[0][0]
    attrdict = results[0][1]
    attrdict['dn'] = dn
    attrdict['uid'] = uid
    # mail
    if 'mail' in attrdict:
        attrdict['mail'] = attrdict['mail'][0].decode(encoding="utf-8")
    else:
        attrdict['mail'] = ''
    # firstName, lastName bereinigen
    for n in ['firstName', 'lastName', 'displayName', 'personalTitle', \
              'uniqueIdentifier', 'givenName', 'sn']:
        l = len(attrdict.get(n, []))
        if l == 0:
            attrdict[n] = ''
        elif l == 1:
            attrdict[n] = attrdict[n][0].decode(encoding="utf-8")
        else:
            # mehrere Einträge, wir nehmen den kürzesten (wg. Umlauten)
            attrdict[n] = _select_attribute(attrdict[n]).decode(encoding="utf-8")
            
    if password:
        # try to bind with dn and password
        try:
            c.simple_bind_s(dn, password)
            attrdict['password_ok'] = True
        except:
            attrdict['password_ok'] = False
    else:
        attrdict['password_ok'] = False
    # cleanup ldap connection
    c.unbind()
    return attrdict

def create_localuser_from_ldapuser(username, ldapUser):
    try:
        localuser = User.objects.get(username=username)
    except User.DoesNotExist:
        localuser = User.objects.create_user(username = username, \
                                             password = '', \
                                             email = ldapUser['mail'])
    localuser.password = 'LDAP_AUTH' # unverschluesselter String
    localuser.email = ldapUser['mail']
    localuser.first_name = _select_attribute([ldapUser['firstName'],
                                              ldapUser['givenName']])
    localuser.last_name = _select_attribute([ldapUser['lastName'],
                                             ldapUser['sn']])
    localuser.is_staff = False
    localuser.is_superuser = False
    localuser.save()
    return localuser