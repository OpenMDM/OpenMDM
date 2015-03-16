# OpenMDM Project

OpenMDM Project is an Open-Source Mobile Device Management project, initially developped to support iOS devices, but built in order to be easily extended with multiple device types.

### Version

0.0.1

### Tech

OpenMDM uses a number of open source projects to work properly:

* [Django](https://www.djangoproject.com/) - HTML enhanced for web apps!
* [Twitter Bootstrap](http://twitter.github.com/bootstrap/) - great UI boilerplate for modern web apps

### Installation


```sh
$ sudo pip install django
$ wget https://pypi.python.org/packages/source/M/MySQL-python/MySQL-python-1.2.5.zip
$ unzip MySQL-python-1.2.5.zip
$ cd MySQL-python-1.2.5
$ python2.7 setup.py build
$ sudo python2.7 setup.py install
$ git clone https://github.com/betezed/MobileDeviceManagement.git OpenMDM
$ cd OpenMDM
```

OpenMDM uses a MySQL database named mdm. Ensure that such a database is created, or change the settings in settings.py  
Once it's done, you can start your server

```sh
$ python manage.py makemigrations public_gate
$ python manage.py migrate
$ python manage.py createsuperuser
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
