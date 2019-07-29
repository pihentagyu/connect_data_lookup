from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q

from . import models

from .utils.data_import import DatasetActions

def get_data(request, data_type):
    '''Import data into models, returning the status in Json'''
    if data_type == 'test':
        return JsonResponse({'data_type': data_type, 'status': 0})
    if data_type != 'postcodes':
        return JsonResponse({'data_type': data_type, 'status': 1, 'error_msg': 'No such datatype. Use postcodes or test'})

    begin_time = datetime.now()
    dataset = DatasetActions(data_type)
    #TO DO: check if data has already been ingested, and if so skip unless ?force=True
    removed = dataset.remove_old()
    #Add number of removed records to json response?
    status, error_msg = dataset.get_dataset()
    if status == 0:
        dataset.add_dataset_to_model() #TO DO: add exceptions, response status
    elapsed_time = datetime.now() - begin_time

    context = {
        'data_type': data_type,
        'status': status,
        'error_msg': str(error_msg),
        'elapsed': elapsed_time.seconds,
    }

    return JsonResponse(context)

class IndexView(TemplateView):
    '''Main index view, shows the records and search form'''
    template_name = 'internet_speed/index.html'
    context_object_name = 'index'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['total_areas'] = models.PostcodeArea.objects.count()
        context['total_codes'] = models.FixedPostcode.objects.count()
        return context

class PostcodeAreaListView(ListView):
    '''List of postcode areas, with links to filter on each'''
    prefetch_related = ('fixedpostcode_set',)
    ordering = ['postcode_area']
    model = models.PostcodeArea
    context_object_name = 'pc_areas'
    paginate_by = 25

    def get_context_data(self):
        context = super().get_context_data()
        return context
    
class FixedPostcodeListView(ListView):
    '''List view of each postcode showing the mean and median upload/download speeds for each'''
    model = models.FixedPostcode
    context_object_name = 'postcodes'
    ordering = ['postcode']
    paginate_by = 25

    def get_queryset(self):
        return models.FixedPostcode.objects.select_related('pc_area').filter(pc_area__postcode_area=self.kwargs['area'])

    def get_context_data(self):
        context = super().get_context_data()
        context['area'] = self.kwargs['area']
        return context

class FixedPostcodeDetailView(DetailView):
    '''Detail view of the internet speeds for a given postcode'''
    context_object_name = 'postcode'
    model = models.FixedPostcode
    template_name = 'internet_speed/postcode_detail.html'
    slug_field = 'postcode'
    def get_object(self):
        return models.FixedPostcode.objects.get(postcode=self.kwargs.get("postcode"))

class SearchResultsView(ListView):
    '''List of search results. Searches can be for parts of the postcode (without spaces) or the entire structured postcode'''
    model = models.FixedPostcode
    context_object_name = 'postcodes'
    paginate_by = 25
    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = models.FixedPostcode.objects.filter(
            Q(postcode__icontains=query) | Q(structured_pc=query) 
        )
        return object_list
