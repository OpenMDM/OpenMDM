#!/bin/bash
printf "Python 3.4 binary [python3.4] "
read -r PYTHON_BINARY
if [ "$PYTHON_BINARY" == "" ]
then
    PYTHON_BINARY="python3.4"
fi
SITE_PACKAGE=$(python3.4 -c 'import site; print(site.getsitepackages()[0])')
mv ./mysql $SITE_PACKAGE
echo "[OK] MySQL connector added"
echo "Creating super user"
$PYTHON_BINARY manage.py createsuperuser
$PYTHON_BINARY manage.py makemigrations public_gate
$PYTHON_BINARY manage.py migrate
