test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=sorokin_test.settings django-admin.py test

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=sorokin_test.settings django-admin.py syncdb --noinput

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=sorokin_test.settings django-admin.py runserver
