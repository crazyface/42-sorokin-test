from django.conf.urls.defaults import patterns, url
import views

urlpatterns = patterns('',
     url(r'^$', views.RequestsListView.as_view(), name='requests'),
)
