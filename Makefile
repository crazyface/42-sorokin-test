test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=sorokin_test.settings django-admin.py test contact core

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=sorokin_test.settings django-admin.py syncdb --noinput
	python sorokin_test/manage.py migrate
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=sorokin_test.settings django-admin.py loaddata sorokin_test/contact/fixtures/*

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=sorokin_test.settings django-admin.py runserver
