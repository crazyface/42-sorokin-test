from django.conf.urls.defaults import patterns, include, url
import views

urlpatterns = patterns('',
     url(r'^$', views.PersonDetailView.as_view(), name='person_detail'),
)
