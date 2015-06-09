from django_auth_ldap.config import LDAPSearch, PosixGroupType
import ldap

"""
This is an example, please update with your own information
"""

CONFIG = dict(
    local=dict(
        database=dict(
            ENGINE='mysql.connector.django',
            NAME='mdm',
            USER='myUser',
            PASSWORD='myPassword',
            HOST='127.0.0.1',
            PORT='3306'),
        ldap=dict(
            SERVER_URI='ldap://myServ.com',
            BIND_DN='cn=John Doe,ou=users,dc=ldap,dc=myServ,dc=com',
            BIND_PASSWORD='myPassword',
            USER_SEARCH=LDAPSearch("ou=users,dc=ldap,dc=myServ,dc=com",
                                   ldap.SCOPE_SUBTREE, "(cn=%(user)s)"),
            GROUP_SEARCH=LDAPSearch("ou=groups,dc=ldap,dc=myServ,dc=com",
                                    ldap.SCOPE_SUBTREE, "(objectClass=posixGroup)"),
            GROUP_TYPE=PosixGroupType(),
            REQUIRE_GROUP='cn=mdm,ou=groups,dc=ldap,dc=myServ,dc=com',
            GROUPS=('finance', 'marketing'),
        ),
        mongo=dict(
            DB='mdm',
        )
    ),
)
