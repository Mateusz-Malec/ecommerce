from django import forms
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

from .models import Computer, Desktop, Laptop


class FilterFormDesktops(forms.Form):
    # system = ModelChoiceField(queryset=Computer.objects.order_by().values_list('system', flat=True).distinct())
    system_choices = Desktop.objects.order_by().values_list('system', 'system').distinct()
    system = forms.MultipleChoiceField(choices=system_choices, widget=forms.CheckboxSelectMultiple, )
    ram_choices = Desktop.objects.order_by().values_list('ram', 'ram').distinct()
    ram = forms.MultipleChoiceField(choices=ram_choices, widget=forms.CheckboxSelectMultiple, )


class FilterFormLaptops(forms.Form):
    # system = ModelChoiceField(queryset=Computer.objects.order_by().values_list('system', flat=True).distinct())
    system_choices = Laptop.objects.order_by().values_list('system', 'system').distinct()
    system = forms.MultipleChoiceField(choices=system_choices, widget=forms.CheckboxSelectMultiple, )
    ram_choices = Laptop.objects.order_by().values_list('ram', 'ram').distinct()
    ram = forms.MultipleChoiceField(choices=ram_choices, widget=forms.CheckboxSelectMultiple, )


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']
