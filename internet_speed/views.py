from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q

from . import models

from .utils.data_import import DatasetActions

# Create your views here.
def get_data(request, data_type):
    '''Import data into models, returning the status in Json'''
    
    if data_type == 'test':
        return JsonResponse({'data_type': data_type, 'status': 0})

    begin_time = datetime.now()
    dataset = DatasetActions(data_type)
    dataset.remove_old()
    status, error_msg = dataset.get_dataset()
    if status == 0:
        dataset.add_dataset_to_model() 
    elapsed_time = datetime.now() - begin_time

    context = {
        'data_type': data_type,
        'status': status,
        'error_msg': str(error_msg),
        'elapsed': elapsed_time.seconds,
    }

    print(context)
    return JsonResponse(context)
    

class IndexView(TemplateView):
    template_name = 'internet_speed/index.html'
    context_object_name = 'index'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['total_areas'] = models.PostcodeArea.objects.count()
        context['total_codes'] = models.FixedPostcode.objects.count()
        return context

class PostcodeAreaListView(ListView):
    prefetch_related = ('fixedpostcode_set',)
    ordering = ['postcode_area']
    model = models.PostcodeArea
    context_object_name = 'pc_areas'
    paginate_by = 25

    def get_context_data(self):
        context = super().get_context_data()
        return context

    
class FixedPostcodeListView(ListView):
    model = models.FixedPostcode
    context_object_name = 'postcodes'
    ordering = ['postcode']
    paginate_by = 25

    def get_queryset(self):
        return models.FixedPostcode.objects.select_related('pc_area').filter(pc_area__postcode_area=self.kwargs['area'])

    def get_context_data(self):
        context = super().get_context_data()
        return context

class FixedPostcodeDetailView(DetailView):
    context_object_name = 'postcode'
    model = models.FixedPostcode
    template_name = 'internet_speed/postcode_detail.html'
    slug_field = 'postcode'
    def get_object(self):
        return models.FixedPostcode.objects.get(postcode=self.kwargs.get("postcode"))

class SearchResultsView(ListView):
    model = models.FixedPostcode
    context_object_name = 'postcodes'
    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = models.FixedPostcode.objects.filter(
            Q(postcode__icontains=query) | Q(structured_pc=query) 
        )
        return object_list
