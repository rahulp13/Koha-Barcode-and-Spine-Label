# Django-Sphinx Documentation

Following are the setup for documenting Django App in Linux (Ubuntu) based Operating System which can be accessed only by Django Admin. It is tested and demonstrated successfully on this platform with Python version >= 3.5 and Django version >= 2.2.

> Note that 'pip' points to the reference of Python3

**I. Installation of Sphinx:**

 - Recommended version >= 2.1.1
 - Open terminal and run the command as: 
 
       sudo pip install Sphinx
       
 - For more information on using Sphinx, see the following reference:
      
       http://www.sphinx-doc.org/en/master/

**II. Installation of Django-Docs:**

 - Recommended version >= 0.3.1
 - Open terminal and run the command as:
 
       sudo pip install django-docs
       
 - For more information on using Sphinx, see the following reference:  
 
       https://pypi.org/project/django-docs/
 
 **III. Installation of Django Decorator-Include:**
  
 - Recommended version >= 2.1
 - Open terminal and run the command as:
 
       sudo pip install django-decorator-include
       
 - For more information on using Sphinx, see the following reference:  
 
       https://pypi.org/project/django-decorator-include/
       
 **IV. Importing Markdown files in Sphinx:**
 
 - Recommended version >= 0.5.0
 - Open terminal and run the command as:
 
       sudo pip install recommonmark
       
 - For more information on using recommonmark, see the following reference:  
 
       https://github.com/rtfd/recommonmark
       
 - Add following snippet in Sphinx's conf.py file:
 
       ...   
       from recommonmark.parser import CommonMarkParser
       ...
       source_parsers = {
         '.md': CommonMarkParser,
       }
       source_suffix = ['.rst', '.md']
       
 **V. Integrating of Sphinx docs on Django Admin:**
 
 - Open following files with root permissions:
   
       1. docs.url - /usr/local/lib/python"your__version__here"/dist-packages/docs/urls.py
       2. docs.views - /usr/local/lib/python"your__version__here"/dist-packages/docs/views.py 
       3. django.contrib.admindocs.urls - /usr/local/lib/python"your__version__here"/dist-packages/django/contrib/admindocs/urls.py 
       4. django.contrib.admindocs.views - /usr/local/lib/python"your__version__here"/dist-packages/django/contrib/admindocs/views.py 
       
 - Copy all the imports from docs.url to django.contrib.admindocs.urls and merge the url patterns of docs.url at the top of the urlpatterns list in the django.contrib.admindocs.urls 
 - Similarly, Copy all the imports, classes and definition from the docs.views to django.contrib.admindocs.views
 - Save the files and close them.
 - Now, in your projects urls.py, Add the following snippet:
 
       ...   
       from django.contrib.admindocs import views
       from decorator_include import decorator_include
       from django.contrib.auth.decorators import user_passes_test
       ...
       
       def check_user(user):
           return user.is_superuser()
           
       urlpatterns = [
            ...
            #Paste the following path above 'admin/' so that there is no conflict
            path('admin/docs/', decorator_include(user_passes_test(lambda u: u.is_superuser), 'django.contrib.admindocs.urls')),
            ...
       ]
       
 - In your projects settings.py, Add the following snippet:
 
       DOCS_ROOT = os.path.join(BASE_DIR, 'your/path/to/root/of/docs/html')
       ...
       INSTALLED_APPS = [
            ...
            'docs',
            ....
       ]
  
