#-*- encoding: utf-8 -*-
'''
Created on 2014年1月26日

@author: ericlin
'''

from django import forms

class ContactForm(forms.Form):
  subject = forms.CharField(max_length=1000)
  email   = forms.EmailField(required = False)
  message = forms.CharField(widget=forms.Textarea)