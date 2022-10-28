from django import forms

from .models import Contact
from .models import User

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ContactForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['issue_description'].required = False
        self.fields['user_name'].required = False
        
    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        no_person = cleaned_data.get('no_person')
        person_no_pii = cleaned_data.get('person_no_pii')
        issue = cleaned_data.get('issue')
        
        skin_color = cleaned_data.get('skin_color')
        hair_color = cleaned_data.get('hair_color')
        face = cleaned_data.get('face')
        gender = cleaned_data.get('gender')
        body_shape = cleaned_data.get('body_shape')
        no_pii = cleaned_data.get('no_pii')
        
        message = cleaned_data.get('issue_description')
        
        label_pii = [skin_color, hair_color, face, gender, body_shape, no_pii]
        check =  False
        for label in label_pii:
            if label is True:
                check = True
                break
        if check == False:
            raise forms.ValidationError('Please select at least one item from column Label PII')
        
        
        if no_person and person_no_pii:
            raise forms.ValidationError('There cannot be no person and a person with no PII', code='invalid')
        
        if issue and len(message) == 0:
            raise forms.ValidationError('If there is an issue, please include a decription', code='invalid')
        
        if (no_person or person_no_pii) and (skin_color or hair_color or face or gender or body_shape):
            raise forms.ValidationError('There cannot be no people and PII exposure', code='invalid')
        
        if no_pii and (skin_color or hair_color or face or gender or body_shape):
            raise forms.ValidationError('There cannot be no PII and PII exposure', code='invalid')
        
        if (person_no_pii and not no_pii):
            raise forms.ValidationError('Must select person no pii and no pii together')  
        
        for key in cleaned_data:
            val = cleaned_data.get(key)
            if type(True) == type(val) and val:
                return cleaned_data
        
        raise forms.ValidationError('Please select at least one checkbox', code='invalid')
        
    class Meta:
        model = Contact
        fields = ['skin_color', 'hair_color', 'face', 'gender', 'body_shape',
                  'no_pii', 'no_person', 'person_no_pii', 'issue', 'issue_description', 'user_name']
        '''
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'input', 'placeholder' : 'Your Name'}),
            'email' : forms.EmailInput(attrs={'class': 'input', 'placeholder' : 'you@email.com'}),
            'message': forms.Textarea(attrs={'class': 'textarea', 'rows': 10, 'placeholder' : 'Your message...'}),
        }
        '''
        widgets = {
            'issue_description': forms.Textarea(attrs={'rows' : 1, 'cols' : 50})
        }
    
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['user_name',]