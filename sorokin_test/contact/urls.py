from django.conf.urls.defaults import patterns, include, url
import views

urlpatterns = patterns('',
     url(r'^$', views.PersonDetailView.as_view(), name='person_detail'),
     url(r'^requests/$', views.RequestsListView.as_view(), name='requests'),
     url(r'^login/$', 'django.contrib.auth.views.login',
            {'template_name': 'contact/login.html'},

            name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
             name='logout'),
)
