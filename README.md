# Koha-Barcode-and-Spine-Label
A Web-Application for searching, selecting and printing barcode and spine labels for the books, records and thesis from a given Koha database.

# Installation and Requirements

Following are the setup for Linux (Ubuntu) based Operating System. The software is tested and demonstrated successfully on this platform.

> Note that 'pip' points to the reference of Python3

**I. Recommended Python version >= 3.5. Install Python first.**
 
 - Use following reference for installation:
 
       http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/

**II. PIP installation for Python:**
 
 - Open terminal and run the command as: 
    
       sudo apt-get install python3-pip
       
**II. PIP installation for Django:**
    
 - Recommend Django version >= 2.2
 - Open terminal and run the command as: 
    
       sudo pip install Django
       
 - Use following reference for more information:
    
       https://docs.djangoproject.com/en/2.2/topics/install/

**III. MySQL connection with Django app:**

 - First thing we will need to do is install python3-dev
 - Open terminal and run the command as: 
 
       sudo apt-get install python3-dev
       
 - Once python3-dev is installed, we can install the necessary Python and MySQL development headers and libraries:
 
       sudo apt-get install python3-dev libmysqlclient-dev
       
 - Then, we will use pip3 to install the mysqlclient library from PyPi. Since our version of pip points to pip3, we can just    use pip:
 
       sudo pip install mysqlclient
 
 **IV. Install django_mysql models:**
 
 - Open terminal and run the command as: 
 
       sudo pip install django-mysql
       
 **V. Install Django Docs:**
 
 - Open terminal and run the command as: 
 
       sudo pip install django-docs
       
 - Use following reference for more information:
 
       https://pypi.org/project/django-docs/
       
 **VI. Install URL Decorator for Django:**
 
 - Open terminal and run the command as: 
 
       sudo pip install django-decorator-include
       
 - Use following reference for more information:
 
       https://github.com/twidi/django-decorator-include
