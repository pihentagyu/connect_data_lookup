import io
import os
import pandas as pd
import requests
import tempfile
from zipfile import ZipFile
#import re

from django.conf import settings
from ..models import PostcodeArea, FixedPostcode
#from django.db import connection, transaction

class DatasetActions:
    def __init__(self, data_type):
        self.data_type = data_type
        self.tempdir = tempfile.TemporaryDirectory()

    def remove_old(self):
        PostcodeArea.objects.all().delete()
        FixedPostcode.objects.all().delete()
        

    def get_dataset(self):
        '''Open dataset file and unizip contents'''
        try:
            data_file = settings.DATASET_FILE
            zipped = ZipFile(io.BytesIO(requests.get(data_file).content))
            zipped.extractall(self.tempdir.name)
        except Exception as e:
            return 1, e
        return 0, None
    
    def add_dataset_to_model(self):
        '''Open each csv file, create a list of dictionaries, add to the database'''
        for fname in os.listdir(self.tempdir.name):
            if os.path.splitext(fname)[1] == '.csv':
                df = pd.read_csv(os.path.join(self.tempdir.name, fname))
                postcode_area = df['postcode area'].iloc[0]
                df = df[['postcode', 
                        'structured postcode', 
                        'Median download speed (Mbit/s)', 
                        'Average download speed (Mbit/s)', 
                        'Median upload speed (Mbit/s)', 
                        'Average upload speed (Mbit/s)'
                ]]
                df.columns = ['postcode', 'structured_pc', 'med_dld_speed', 'avg_dld_speed', 'med_upld_speed', 'avg_upld_speed']
                df.fillna(-1, inplace=True)
                postcode_dict_list = df.to_dict(orient='records')
                
                PostcodeArea.objects.create(postcode_area=postcode_area)
                PostcodeArea.objects.last().add_postcodes(postcode_dict_list)


