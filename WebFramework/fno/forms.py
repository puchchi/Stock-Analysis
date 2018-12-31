import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django import forms
from option.models import kOptionValueFormModel

class kOptionValueForm(forms.ModelForm):
    optionStock = forms.CharField(max_length=256, help_text="Enter stock name with expiry")
    expiryMonth = forms.CharField(max_length=3, help_text="Enter expiry month")
    expiryYear = forms.IntegerField(min_value=2010, help_text="Enter expiry year")

    class Meta:
        model = kOptionValueFormModel
        fields = '__all__'