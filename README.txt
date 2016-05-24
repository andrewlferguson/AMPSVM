--1-- local setup

Create and load virtual environment:
>> sudo conda create -n AMPSVM python=2.7 anaconda
>> source activate AMPSVM
>> conda info --envs
>> python --version


Install django and sklearn into virtual environment:
>> sudo conda install -n AMPSVM django
>> sudo conda install -n AMPSVM scikit-learn=0.16.0


Installing propy into virtual environment:

   &&& propy contains errors in CTD descriptor calculations &&&

   Must manually modify propy-1.0/src/propy/CTD.py to contain correct aa's in each group
   as per A_Li et al. [PROFEAT] (2006); appears to be an error in transcribing the aa 	
   groups for polarity, and a missing entry for C in the Li paper

>> tar -zxf propy-1.0.tar.gz
>> cd propy-1.0

-> Manually repair ./propy-1.0/src/propy/CTD.py

>> sudo python setup.py install


Testing SVM prediction:

>> python descripGen_12.py './aaindex/' 'seqs.txt' 1 1
>> python predictSVC.py 'descriptors.csv' 'Z_score_mean_std__intersect_noflip.csv' 'svc.pkl'


Construct site:
>> django-admin startproject mysite .

Modify mysite/settings.py:
(i) Edit: TIME_ZONE = 'US/Central'
(ii) Add as final line below STATIC_URL: STATIC_ROOT = os.path.join(BASE_DIR, 'static')

Migrate:
>> python manage.py migrate

Test:
>> python manage.py runserver

Create app:
>> python manage.py startapp svm

Modify mysite/settings.py:
(i) Add 'svm' to INSTALLED_APPS 

Migrate:
>> python manage.py makemigrations svm
>> python manage.py migrate svm

Initialize git:
>> git init
>> git config --global user.name "Andrew Ferguson"
>> git config --global user.email andrew.l.ferguson@gmail.com

>> echo "*.pyc
__pycache__
db.sqlite3
/static
.DS_Store" > .gitignore

>> git status
>> git add --all .
>> git commit -m "My AMPSVM app, first commit"


GitHub:
Login to GitHub.com.
Create a new repository named "AMPSVM". 
Leave the "initialize with a README" tickbox un-checked, leave the .gitignore option blank (we've done that manually) and leave the License as None.

>> git remote add origin https://github.com/andrewlferguson/AMPSVM.git
>> sudo git push --set-upstream origin master
>> sudo git push


--2-- Python Anywhere setup

Python Anywhere:
Login to PythonAnywhere.com
Boot bash console
> git clone https://github.com/andrewlferguson/AMPSVM.git
> tree AMPSVM
> cd AMPSVM
> virtualenv --python=python2.7 AMPSVM
> source AMPSVM/bin/activate

> cd propy-1.0
> rm -r build
> python setup.py install
> cd ..

> pip install numpy
> pip install scipy
> pip install scikit-learn==0.16.0
> pip install django~=1.9.0
> pip install urllib3[secure] pyopenssl ndg-httpsclient pyasn1


## NOTE ## 
Installation of these modules requires more disk space than is available on the free 512 MB "Beginner" account -- needed to upgrade to "Hacker" to install. BUT post-
installation disc space fits within 512 MB so can probably downgrade after virtual environment is set up.


Testing SVM prediction:

> python descripGen_12.py "./aaindex/" 'seqs.txt' 1 1
> python predictSVC.py 'descriptors.csv' 'Z_score_mean_std__intersect_noflip.csv' 'svc.pkl'


> python manage.py migrate
> python manage.py createsuperuser

Click back to the PythonAnywhere dashboard by clicking on its logo.
Click on the Web tab.
Hit Add a new web app.
After confirming your domain name, choose manual configuration (NOT the "Django" option) in the dialog. 
Choose Python 2.7, and click Next to finish the wizard.

In the "Virtualenv" section, click red text "Enter the path to a virtualenv", and enter: 
/home/andrewlferguson/AMPSVM/AMPSVM/
Click the blue box with the check mark to save the path.

Click on the "WSGI configuration file" link (in the "Code" section near the top of the page -- it'll be named something like /var/www/<your-PythonAnywhere-username>_pythonanywhere_com_wsgi.py), and you'll be taken to an editor.

Delete all the contents and replace them with this:

"""
import os
import sys

path = '/home/andrewlferguson/AMPSVM'  # use your own PythonAnywhere username here
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(get_wsgi_application())
"""

Hit Save and then go back to the Web tab.

We're all done! Hit the big green Reload button and you'll be able to go view your application. You'll find a link to it at the top of the page.

The default page for your site should say "Welcome to Django", just like it does on your local computer. Try adding /admin/ to the end of the URL, and you'll be taken to the admin site. 


--3-- local -> git -> deploy loop

Local edits:

Modify mysite/urls.py (see file)

Create svm/urls.py (see file)

Create svm/forms.py (see file)

Modify svm/views.py (see file)

Create directory svm/templates
Create directory svm/templates/svm
Create file svm/templates/svm/name.html (see file)
Create file svm/templates/svm/thanks.html (see file)
Create file svm/templates/svm/base.html (see file)

Create directory svm/static
Create directory svm/static/css
Create file svm/static/svm.css

Github push:
>> git status
>> git add --all .
>> git commit -m ""
>> sudo git push

PythonAnywhere pull:
> git pull
Reload webpage

	PythonAnywhere hard pull and reset:
	> git fetch --all
	> git reset --hard origin/master
	> git pull



# Python Anywhere NOTES #

1. Installation of {numpy, scipy, sklearn} modules into virtual environment requires more disk space than is available on the free 512 MB "Beginner" account -- needed to upgrade to "Hacker" to install. BUT post-installation disc space fits within 512 MB so can probably downgrade after virtual environment is set up.

2. PythonAnywhere employs different cwd than local implementation 
- local cwd is ~/AMPSVM
- PythonAnywhere cwd runs inside virtual environment ~/AMPSVM/AMPSVM

So must change the following lines in svm/views.py:

sys.path.append('./code') 				-> 	sys.path.append('./AMPSVM/code')
os.chdir('./code')					-> 	os.chdir('./AMPSVM/code')
descripGen_12.main('./aaindex','../seqs.txt',1,1)	-> 	descripGen_12.main('./aaindex','../../seqs.txt',1,1)
os.chdir('..')						-> 	os.chdir('../..')

For convenience have hosted two views.py files (i) views_localhost.py and (ii) views_PythonAnywhere.py 

Pull from git then manually within PythonAnywhere 
- delete views.py 
- edit and save as views_PythonAnywhere.py -> views.py







Deactivate virtual environment:
>> source deactivate

#Delete virtual environment:
#>> sudo conda remove -n AMPSVM -all













