from django.db import models


class PostcodeArea(models.Model):
   postcoode_area = models.CharField(max_length=2)

   def add_postcodes(self, postcode_dict_list):
        '''Method for populating the FixedPostcode model for a given postcode area'''
        postcode_list = [FixedPostcode(doc=self, **postcode) for postcode in postcode_dict_list]
        self.sentence_set.bulk_create(postcode_list)

class FixedPostcode(models.Model):
    '''Fixed Postcode table'''
    postcode = models.CharField(max_length=7)
    structured_pc = models.CharField(max_length=8)
    pc_area = models.ForeignKey(PostcodeArea, on_delete=models.CASCADE)
    med_dld_speed = models.SmallIntegerField()
    avg_dld_speed = models.SmallIntegerField()
    med_upld_speed = models.SmallIntegerField()
    avg_upld_speed = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    

