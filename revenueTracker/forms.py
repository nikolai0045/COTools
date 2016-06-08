from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, ButtonHolder
from crispy_forms.bootstrap import FormActions
from .models import Student, CashPayment, CheckPayment

def get_student_list():
	student_return = []
	students = Student.objects.all()
	for student in students:
		student_name = student.first_name + ' ' + student.last_name
		student_pk = student.pk
		student_data = (student_pk,student_name)
		student_return.append(student_data)
	student_return = tuple(student_return)
	return student_return

class BeginReportForm(forms.Form):
	
	def __init__(self,*args,**kwargs):
		
		super (BeginReportForm,self).__init__(*args,**kwargs)
		
		self.fields['student_name'] = forms.TypedChoiceField(
			choices = get_student_list(),
			required = True,
		)
		
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Div(
				'student_name',
			),
			FormActions(
				Submit('submit','Create Report', css_class='btn btn-default'),
			),
		)
		
class EditReportForm(forms.Form):
	
	def __init__(self,*args,**kwargs):
		
		super (EditReportForm,self).__init__(*args,**kwargs)
		
		
class AddCashGiftForm(forms.Form):
	
	def __init__(self,*args,**kwargs):
		report_pk = kwargs.pop('report_pk')
		student_pk = kwargs.pop('student_pk')
		gift_pk = kwargs.pop('gift_pk',False)
		
		super (AddCashGiftForm,self).__init__(*args,**kwargs)
		
		self.fields['amount'] = forms.IntegerField()
		self.fields['salutation'] = forms.CharField(max_length=10,required=False)
		self.fields['first_name'] = forms.CharField(max_length=20, required=False)
		self.fields['last_name'] = forms.CharField(max_length=20, required=True)
		self.fields['street_address'] = forms.CharField(max_length=40, required=False)
		self.fields['city'] = forms.CharField(max_length=40, required=False)
		self.fields['state'] = forms.CharField(max_length=2, required=False)
		self.fields['zip_code'] = forms.CharField(max_length=10,required=False)
		self.fields['report_pk'] = forms.IntegerField(initial=report_pk, widget=forms.HiddenInput())
		self.fields['student_pk'] = forms.IntegerField(initial=student_pk,widget=forms.HiddenInput())
		
		if gift_pk:
			gift = CashPayment.objects.get(pk=gift_pk)
			self.fields['amount'].initial = gift.amount
			self.fields['salutation'].initial = gift.salutation
			self.fields['first_name'].initial = gift.first_name
			self.fields['last_name'].initial = gift.last_name
			self.fields['street_address'].initial = gift.street_address
			self.fields['city'].initial = gift.city
			self.fields['state'].initial = gift.state
			self.fields['zip_code'].initial = gift.zip_code
			
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Div(
				'salutation',
				'first_name',
				'last_name',
				'street_address',
				'city',
				'state',
				'zip_code',
				'amount',
				'report_pk',
				'student_pk',
				'gift_pk',
			),
			FormActions(
				Submit('submit','Add this gift', css_class='btn btn-default'),
			),
		)

class AddCheckGiftForm(AddCashGiftForm):
	
	def __init__(self,*args,**kwargs):
		
		super (AddCheckGiftForm,self).__init__(*args,**kwargs)
		
		self.fields['check_number'] = forms.CharField(max_length=20,required=False)
		
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Div(
				'salutation',
				'first_name',
				'last_name',
				'street_address',
				'city',
				'state',
				'zip_code',
				'amount',
				'check_number',
				'report_pk',
				'student_pk',
				'gift_pk',
			),
			FormActions(
				Submit('submit','Add this gift',css_class='btn btn-default'),
			),
		)
