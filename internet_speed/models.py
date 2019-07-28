from django.db import models


class PostcodeArea(models.Model):
   postcode_area = models.CharField(unique=True, max_length=2)

   def add_postcodes(self, postcode_dict_list):
        '''Method for populating the FixedPostcode model for a given postcode area'''
        postcode_list = [FixedPostcode(pc_area=self, **postcode) for postcode in postcode_dict_list]
        self.fixedpostcode_set.bulk_create(postcode_list)

class FixedPostcode(models.Model):
    '''Fixed Postcode table'''
    postcode = models.CharField(unique=True, max_length=7)
    structured_pc = models.CharField(max_length=8)
    pc_area = models.ForeignKey(PostcodeArea, on_delete=models.CASCADE)
    med_dld_speed = models.DecimalField(max_digits=5, decimal_places=1)
    avg_dld_speed = models.DecimalField(max_digits=5, decimal_places=1)
    med_upld_speed = models.DecimalField(max_digits=4, decimal_places=1)
    avg_upld_speed = models.DecimalField(max_digits=4, decimal_places=1)
    created = models.DateTimeField(auto_now_add=True)

    

