import datetime

from django import forms
from Myapp.models import Order, Student


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


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='username', max_length=100)
    password = forms.CharField(required=True, label='password', max_length=20)


class Register(forms.ModelForm):
    password2 = forms.CharField(required=True, label='confirm Password')

    class Meta:
        model = Student
        fields = ['avatar', 'username', 'password', 'first_name', 'last_name', 'email',
                  'school', 'address', 'city', 'interested_in']
        widgets = {'interested_in': forms.CheckboxSelectMultiple, 'password': forms.PasswordInput,
                   'avatar': forms.ClearableFileInput}
        labels = {'school': 'school', 'password': 'Input password', 'city': 'city', 'address': 'address',
                  'interested_in': 'Topics you are interested in'}


class pwdReset(forms.Form):
    email = forms.EmailField(help_text='Please input your email, then click send')
