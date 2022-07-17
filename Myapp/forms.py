import datetime

from django import forms
from Myapp.models import Order

class InterestForm(forms.Form):
    interested = forms.ChoiceField(choices=(('1', 'Yes'), ('2', 'No')), widget=forms.RadioSelect)
    levels = forms.IntegerField(initial=1, min_value=1)
    comments = forms.CharField(required=False, label='Additional Comments', widget=forms.Textarea)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student', 'course', 'levels', 'order_date']
        widgets = {'student': forms.RadioSelect, 'order_date': forms.SelectDateWidget}
        initial = {'order_date': datetime.date}
        labels = {'student': 'student_label', 'course': 'course_label'}

class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='username', max_length=100)
    password = forms.CharField(required=True, label='password', max_length=20)
