from django.test import TestCase, Client
from django.utils import timezone

from .models import *
from .views import *

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

