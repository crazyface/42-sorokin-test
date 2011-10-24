test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=sorokin_test.settings django-admin.py test contact

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=sorokin_test.settings django-admin.py syncdb --noinput
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=sorokin_test.settings django-admin.py loaddata sorokin_test/contact/fixtures/*

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=sorokin_test.settings django-admin.py runserver
