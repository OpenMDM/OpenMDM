#!/bin/bash
PYTHON3_DEFAULT_PATH=$(which python3)
echo -ne "Please enter the path to Python 3.4 "
if [ ! -z ${PYTHON3_DEFAULT_PATH} ]
then
    echo -ne "[default ${PYTHON3_DEFAULT_PATH}] "
fi
read PYTHON3_PATH
if [ -z ${PYTHON3_PATH} ]
then
    PYTHON3_PATH=${PYTHON3_DEFAULT_PATH}
fi
CHECK_VERSION=$(${PYTHON3_PATH} -c 'import sys; print(sys.version_info[:2])' 2>/dev/null)
if [ "${CHECK_VERSION}" != "(3, 4)" ]
then
    echo  "Invalid Python interpreter, version 3.4 required"
    exit -1
fi
SITE_PACKAGE=$(${PYTHON3_PATH} -c 'import site; print(site.getsitepackages()[0])')
mv ./mysql ${SITE_PACKAGE} 2>/dev/null
echo "[OK] MySQL connector added"
echo "Creating super user"
${PYTHON3_PATH} manage.py createsuperuser
${PYTHON3_PATH} manage.py makemigrations public_gate
${PYTHON3_PATH} manage.py migrate
