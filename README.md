# OpenMDM Project

OpenMDM Project is an Open-Source Mobile Device Management project, initially developed to support iOS devices, but built in order to be easily extended with multiple device types.  
Language : Python 3.4  
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

### Architecture

![alt tag](http://hackndo.com/archi.jpg) 

### Requirements

* [Python 3.4](https://www.python.org/downloads/release/python-343/)
* [Django 1.7](https://docs.djangoproject.com/fr/1.7/topics/install/)
* [MongoDB](https://www.mongodb.org/)

### Installation


```sh
$ pip3.4 install django-admin-bootstrapped
$ pip3.4 install git+https://github.com/rbarrois/python-ldap.git@py3
$ pip3.4 install django-auth-ldap
$ pip3.4 install mongoengine
$ git clone https://github.com/betezed/MobileDeviceManagement.git OpenMDM
$ cd OpenMDM
$ sudo ./configure.sh
$ python manage.py runserver
```
OpenMDM is now listening on port 8000.
You can set a custom port and accept connexions from any IP addresses

```sh
$ python manage.py runserver 0.0.0.0:1337
```


### Development

Want to contribute? Great, feel free !


### Examples

[Home page](http://hackndo.com:8000)  
[Admin page](http://hackndo.com:8000/admin/)

