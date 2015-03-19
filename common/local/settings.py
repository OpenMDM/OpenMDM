CONFIG = dict(
    local=dict(
        database=dict(
            ENGINE='mysql.connector.django',
            NAME='mdm',
            USER='root',
            PASSWORD='root',
            HOST='127.0.0.1',
            PORT='8889'),
        ldap=dict(
            AUTH_LDAP_URI='ldap://hackndo.com:389',
            AUTH_LDAP_BASE_DN='ou=users,dc=ldap,dc=hackndo,dc=com',
        )
    ),
)