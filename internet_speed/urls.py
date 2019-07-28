from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'internet_speed'

urlpatterns = [
        #url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^get_data/(?P<data_type>[\w\-]+)/$', views.get_data, name='get_data'),
        url(r'^pc_areas/$', views.PostcodeAreaList.as_view(), name='pc_areas_list'),
        url(r'^pc_areas/(?P<area>\w{1,2})/$', views.FixedPostcodeList.as_view(), name='fixed_pc_list'),
        url(r'^postcodes/(?P<area>\w{7})/$', views.FixedPostcodeList.as_view(), name='fixed_pc_detail'),


]
