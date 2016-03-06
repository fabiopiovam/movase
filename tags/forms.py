# -*- coding: utf-8 -*-
from django import forms
from tags import get_tags

class FormTags(forms.ModelForm):
    
    tags = forms.CharField(max_length=400, required=False, help_text=u"Digite as palavras-chave separadas por vírgula")
    
    def __init__(self, *args, **kwargs):
        super(FormTags, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.initial['tags'] = get_tags(self.instance)