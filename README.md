# OpenMDM Project

OpenMDM Project is an Open-Source Mobile Device Management project, initially developed to support iOS devices, but built in order to be easily extended with multiple device types.  
It's written in Python 3.4 (and needs to be used with Python 3.X)

### Version

0.0.1

### Tech

OpenMDM uses open source projects to work properly:

* [Django](https://www.djangoproject.com/)  
* [Django Python3 LDAP](https://pypi.python.org/pypi/django-python3-ldap/0.9.1)
* [Django admin bootstrapped](https://pypi.python.org/pypi/django-admin-bootstrapped/)
* [Twitter Bootstrap](http://twitter.github.com/bootstrap/)  

### Architecture

![alt tag](http://hackndo.com/archi.jpg) 

### Installation

Requirements :  

* [Python 3.4](https://www.python.org/downloads/release/python-343/)
* [Django 1.7](https://docs.djangoproject.com/fr/1.7/topics/install/)
* [MySQL](http://www.mysql.com/downloads/) with *mdm* database
* [MySQL - Python connector](https://pypi.python.org/pypi/mysql-connector-python/2.0.3)

```sh
$ pip3.4 install django-admin-bootstrapped
$ pip3.4 install django-python3-ldap
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

