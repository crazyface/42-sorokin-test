from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
import views

urlpatterns = patterns('',
     url(r'^$', views.RequestsListView.as_view(), name='requests'),
)
