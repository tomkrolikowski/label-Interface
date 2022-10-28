from django.db import models
import numpy as np
import os

class Contact(models.Model):
    # PURPOSE_CHOICES = [
    #     ('IN', 'Inquiry'),
    #     ('CO', 'Complaint'),
    #     ('FB', 'Feedback'),
    # ]

    # name = models.CharField(max_length=100)
    # email = models.EmailField(max_length=100)
    # purpose = models.CharField(max_length=2, choices=PURPOSE_CHOICES)
    # message = models.TextField()
    photo_name = ""
    skin_color = models.BooleanField()
    hair_color = models.BooleanField()
    face = models.BooleanField()
    gender = models.BooleanField()
    body_shape = models.BooleanField()
    no_person = models.BooleanField()
    person_no_pii = models.BooleanField()
    issue = models.BooleanField()
    no_pii = models.BooleanField()
    issue_description = models.TextField()
    user_name = models.CharField(max_length=20, help_text='Name')
    
    
    def save(self, *args, **kwargs):
        print(self.photo_name, "saved")
        self.photo_name += '_' + self.user_name
        items = [self.skin_color, self.hair_color, self.face, 
                 self.gender, self.body_shape, self.no_pii, self.no_person,
                 self.person_no_pii, self.issue]
        if self.issue:
            base_name = os.path.basename(self.photo_name) 
            base_name = os.path.splitext(base_name)[0]
            name = 'issues/' + os.path.basename(self.photo_name) + '.txt'
            with open(name, 'w') as f:
                f.write(self.issue_description)
        np.savez(self.photo_name , np.array(items))
        
class User(models.Model):
    photo_name = "" 
    user_name = models.CharField(max_length=20, help_text='Name')