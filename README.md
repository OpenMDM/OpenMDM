# OpenMDM Project

OpenMDM Project is an Open-Source Mobile Device Management project, initially developed to support iOS devices, but built in order to be easily extended with multiple device types.  
It's written in Python 3.4 (and needs to be used with Python 3.X)

### Version

0.0.1

### Tech

OpenMDM uses open source projects to work properly:

* [Django](https://www.djangoproject.com/)  
* [Twitter Bootstrap](http://twitter.github.com/bootstrap/)  

### Installation


```sh
$ sudo pip3.4 install django
$ git clone https://github.com/betezed/MobileDeviceManagement.git OpenMDM
$ cd OpenMDM
```

OpenMDM uses a MySQL database named mdm. Ensure that such a database is created, or change the settings in settings.py  
Once it's done, you can configure your application and start your server.

```sh
$ sudo ./configure.sh # sudo, because it needs write permissions in python 3.4 "site-packages" directory
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
