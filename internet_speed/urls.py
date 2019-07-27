from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'internet_speed'

urlpatterns = [
        #url(r'^$', views.IndexView.as_view(), name='index'),
        #url(r'^get_data/<data_type:slug>', views.get_data, name='get_data'),
        url(r'^get_data/(?P<data_type>[\w\-]+)/$', views.get_data, name='get_data'),

]
