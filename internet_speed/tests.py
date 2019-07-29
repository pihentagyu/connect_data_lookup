from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

import json
import mock
import tempfile
import unittest
from unittest.mock import MagicMock

from .models import *
from .views import *
#from .utils.data_import import DatasetActions
from .utils import data_import

class PostcodeAreaTests(TestCase):
    def setUp(self):
        self.postcode_area = PostcodeArea.objects.create(
                postcode_area = 'AB',
            )

        self.postcode_area.save()
        self.postcode_dict_list = [{'postcode': 'AB101AL',
          'structured_pc': 'AB10 1AL',
          'med_dld_speed': -1.0,
          'avg_dld_speed': -1.0,
          'med_upld_speed': -1.0,
          'avg_upld_speed': -1.0},
         {'postcode': 'AB101AN',
          'structured_pc': 'AB10 1AN',
          'med_dld_speed': -1.0,
          'avg_dld_speed': -1.0,
          'med_upld_speed': -1.0,
          'avg_upld_speed': -1.0},
         {'postcode': 'AB101AP',
          'structured_pc': 'AB10 1AP',
          'med_dld_speed': -1.0,
          'avg_dld_speed': -1.0,
          'med_upld_speed': -1.0,
          'avg_upld_speed': -1.0},
         {'postcode': 'AB101AS',
          'structured_pc': 'AB10 1AS',
          'med_dld_speed': -1.0,
          'avg_dld_speed': -1.0,
          'med_upld_speed': -1.0,
          'avg_upld_speed': -1.0},
         {'postcode': 'AB101AU',
          'structured_pc': 'AB10 1AU',
          'med_dld_speed': 15.7,
          'avg_dld_speed': 15.5,
          'med_upld_speed': 1.1,
          'avg_upld_speed': 1.0}]
        self.postcode = FixedPostcode.objects.create(
                pc_area = self.postcode_area,
                **self.postcode_dict_list[0]
                )
        self.postcode.save()

    def test_postcode_area_creation(self):
        postcode_area = PostcodeArea.objects.last()
        self.assertEqual(PostcodeArea.objects.last().postcode_area, 'AB')

    def test_postcode_creation(self):
        self.assertLess(self.postcode.created, timezone.now())
        postcodes = [v['postcode'] for v in self.postcode_area.fixedpostcode_set.all().values()]
        self.assertIn('AB101AL', postcodes)

    def test_add_postcodes(self):
        FixedPostcode.objects.all().delete()
        self.postcode_area.add_postcodes(self.postcode_dict_list)
        postcodes = FixedPostcode.objects.all()
        self.assertEqual(postcodes[1].postcode, 'AB101AN')
        self.assertEqual(postcodes[4].avg_dld_speed, 15.5)
        self.assertEqual(postcodes[0].pc_area.postcode_area,'AB')

class DatasetActionsTest(unittest.TestCase):
    def setUp(self):
        self.dataset_actions = data_import.DatasetActions('test')
        self.assertEqual(self.dataset_actions.data_type, 'test')
        self.assertIsInstance(self.dataset_actions.tempdir, tempfile.TemporaryDirectory)

    def test_remove_old(self):
        data_import.PostcodeArea = MagicMock()
        #return_value=(1605068, {'internet_speed.FixedPostcode': 1604947, 'internet_speed.PostcodeArea': 121}))
        resp = self.dataset_actions.remove_old()
        self.assertIsInstance(resp, MagicMock)
        data_import.PostcodeArea.objects.all().delete.assert_called()
        
    def test_get_dataset(self):
        data_import.ZipFile = MagicMock()
        data_import.requests = MagicMock()
        data_import.io = MagicMock()
        resp = self.dataset_actions.get_dataset()
        data_import.io.BytesIO.assert_called() 
        data_import.ZipFile.assert_called()
        data_import.requests.get.assert_called_with('https://www.ofcom.org.uk/static/research/connected-nations2016/2016_fixed_pc_r01.zip')
        self.assertEqual(resp[0], 0)
        self.assertEqual(resp[1], None)

        data_import.requests.get = MagicMock(side_effect=Exception('Fail!'))
        resp = self.dataset_actions.get_dataset()
        self.assertEqual(resp[0], 1)
        self.assertIsInstance(resp[1], Exception)
        data_import.requests.get.assert_called_with('https://www.ofcom.org.uk/static/research/connected-nations2016/2016_fixed_pc_r01.zip')

    def add_dataset_to_model(self):
        self.dataset_actions.tempdir = MagicMock()
        self.dataset_actions.add_dataset_to_model()
        self.dataset_actions.tempdir.name.assert_called()
        



class InternetSpeedViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.postcode_area = PostcodeArea.objects.create(
                postcode_area = 'AB',
            )
        self.postcode_area.save()
        self.postcode_dict_list = [{'postcode': 'AB101AL',
          'structured_pc': 'AB10 1AL',
          'med_dld_speed': -1.0,
          'avg_dld_speed': -1.0,
          'med_upld_speed': -1.0,
          'avg_upld_speed': -1.0},
         {'postcode': 'AB101AN',
          'structured_pc': 'AB10 1AN',
          'med_dld_speed': -1.0,
          'avg_dld_speed': -1.0,
          'med_upld_speed': -1.0,
          'avg_upld_speed': -1.0},
         {'postcode': 'AB101AP',
          'structured_pc': 'AB10 1AP',
          'med_dld_speed': -1.0,
          'avg_dld_speed': -1.0,
          'med_upld_speed': -1.0,
          'avg_upld_speed': -1.0},
         {'postcode': 'AB101AS',
          'structured_pc': 'AB10 1AS',
          'med_dld_speed': -1.0,
          'avg_dld_speed': -1.0,
          'med_upld_speed': -1.0,
          'avg_upld_speed': -1.0},
         {'postcode': 'AB101AU',
          'structured_pc': 'AB10 1AU',
          'med_dld_speed': 15.7,
          'avg_dld_speed': 15.5,
          'med_upld_speed': 1.1,
          'avg_upld_speed': 1.0}]
        self.postcode = FixedPostcode.objects.create(
                pc_area = self.postcode_area,
                **self.postcode_dict_list[0]
                )
        self.postcode.save()

        #self.index_view = IndexView()

    def test_get_data_view(self):
        #dataset_actions = DatasetActions('test')
        resp = self.client.get(reverse('internet_speed:get_data' , kwargs={'data_type':'test'}))
        self.assertEqual(resp.status_code, 200)

        content = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(content['data_type'], 'test')
        self.assertEqual(content['status'], 0)
        
    #def test_index_page(self):
    #    resp = self.client.get(reverse('internet_speed:index'))
    #    self.assertEqual(resp.status_code, 200)
    #    #self.assertEqual(resp.context['total_docs'], 1)

    def test_list_postcode_view(self):
        resp = self.client.get(reverse('internet_speed:pc_areas_list'))
        self.assertEqual(resp.status_code, 200)
        print(resp)

    def test_list_postcode_view(self):
        resp = self.client.get(reverse('internet_speed:fixed_pc_list', kwargs={'area': 'AB'}))
        self.assertEqual(resp.status_code, 200)
        print(resp)
