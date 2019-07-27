from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .utils.data_import import DatasetActions

# Create your views here.
def get_data(request, data_type):
    '''Import data into models, returning the status in Json'''
    
    if data_type == 'test':
        return JsonResponse({'data_type': data_type, 'status': 0})

    begin_time = datetime.now()
    dataset = DatasetActions(data_type)
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
    
