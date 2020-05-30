from django.forms import ModelForm
from django import forms

priorities = ((1, 'High'), (2, 'Medium'), (3, 'Low'))

class TodoForm(forms.Form):
    text = forms.CharField(
        max_length=100,
        widget=forms.TextInput( attrs={ 
            'class': 'form-control ',
            'style':'width: 500px;',
            'placeholder': 'Click and Tell your Task Eg: "go to gym high priority"',
            'id':'speechToText',
            'onclick':'record()'
            })
            )


    priority = forms.CharField(
        label='Task Priority: ',
        required=True,
        widget=forms.RadioSelect(choices=priorities, attrs={'class': 'radiabtn'})
            )  

class MailTodoForm(forms.Form):
    content = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Enter Additional Message for the Mail..',
                                        'class': 'form-control'})
        )
    
    
    mailtoself = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'id':'mailToSelfBtn'})
        )

    mailid = forms.CharField(
        initial="",
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                        'placeholder': 'Enter Email Address to be sent to..',
                                        'id':'mailid'})
                                        )