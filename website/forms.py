from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record, Order
from .models import Drug
from django.core.validators import RegexValidator
class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control form-control-lg'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control form-control-lg'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control form-control-lg'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	




# Create Add Record Form
class AddRecordForm(forms.ModelForm):


	customer_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"customer Name", "class":"form-control"}), label="")
	customer_phone_number = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
	customer_address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="")
	#drug_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"drug", "class":"form-control"}), label="")
	#price = forms.DecimalField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "price", "class": "form-control"}), label="")
	quantity_sold  = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "quantity", "class": "form-control"}), label="")
	#drug_name = forms.ChoiceField(choices=)
	price = forms.DecimalField(widget=forms.HiddenInput(),initial=0.0)

	class Meta:
		model = Record
		exclude = ("user",)

class DrugForm(forms.ModelForm):

	drug_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"drug", "class":"form-control"}), label="")
	price = forms.DecimalField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "price", "class": "form-control"}),label="")
	quantity_purchased = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "quantity", "class": "form-control"}), label="")
	expire_date = forms.DateField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "expire date(2023-11-01)", "class": "form-control"}), label="")


	class Meta:
		model = Drug
		exclude = ("user",)

class SearchForm(forms.Form):
    query = forms.CharField(label='Search')

class Orderform(forms.ModelForm):
	#drug_name= forms.ModelChoiceField(queryset=Drug.objects.filter(to_field_name='drug_name'))
	drug_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"drug", "class":"form-control"}), label="")
	price = forms.DecimalField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "price", "class": "form-control"}),label="")
	quantity = forms.IntegerField(required=True,widget=forms.widgets.TextInput(attrs={"placeholder": "price", "class": "form-control"}),label="")
	supplier_phone = forms.IntegerField(required=True,widget=forms.widgets.TextInput(attrs={"placeholder": "Phone", "class": "form-control"}),label="")
	supplier_address = forms.CharField(required=True,widget=forms.widgets.TextInput(attrs={"placeholder": "Address", "class": "form-control"}),label="")
	supplier_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}), label="")


	class Meta:
		model = Order
		exclude = ("user",)
