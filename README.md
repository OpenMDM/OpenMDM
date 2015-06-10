# OpenMDM Project

OpenMDM Project is an Open-Source Mobile Device Management project, initially developed to support iOS devices, but built in order to be easily extended with multiple device types.  
Language : Python 3.4.2 and >  
Authentication : LDAP3  
Storage : MongoDB  

### Version

0.0.1

### Tech

OpenMDM uses open source projects to work properly:

* [Django](https://www.djangoproject.com/)  
* [Django Auth Ldap](https://pypi.python.org/pypi/django-auth-ldap/1.2.5)
* [MongoEngine](https://pypi.python.org/pypi/mongoengine/0.8.7)
* [Django admin bootstrapped](https://pypi.python.org/pypi/django-admin-bootstrapped/)
* [Twitter Bootstrap](http://twitter.github.com/bootstrap/)  

### Requirements

* [Python 3.4.2 and >](https://www.python.org/downloads/release/python-343/)
* [Django 1.7](https://docs.djangoproject.com/fr/1.7/topics/install/)
* [MongoDB](https://www.mongodb.org/)  

Also, OpenMDM require a LDAP service for accounts management.

### Installation

#### Prepare Debian 8
```sh
sudo apt-get install libldap2-dev
sudo apt-get install libsasl2-dev
sudo apt-get install python3.4
sudo apt-get install mongodb
sudo apt-get install mysql-server
```

#### For all systems

Create a MySQL database and user
```mysql
CREATE DATABASE mdmdb;
GRANT ALL PRIVILEGES ON mdmdb.* TO 'mdmuser@localhost' IDENTIFIED BY 'MDMPassword123';
```

```sh
cd /usr/local
virtualenv -p python3.4 OpenMDM_VEnv
cd OpenMDM_VEnv
source ./bin/activate
pip3.4 install django-admin-bootstrapped
pip3.4 install git+https://github.com/rbarrois/python-ldap.git@py3
pip3.4 install django-auth-ldap
pip3.4 install mongoengine
git clone https://github.com/betezed/MobileDeviceManagement.git OpenMDM
cd OpenMDM
```
Now your system is ready, you must customize the common/local/settings.py values to fit your deployment.

```sh
sudo ./configure.sh
python manage.py runserver
```
OpenMDM is now listening on port 8000.
You can set a custom port and accept connexions from any IP addresses

### Development

Want to contribute? Great, feel free !
