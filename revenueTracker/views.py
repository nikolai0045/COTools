from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Student, Report, CheckPayment, CashPayment
from .forms import BeginReportForm, AddCashGiftForm, AddCheckGiftForm

# Create your views here.
	
class StudentHome(View):
	
	template = 'revenueTracker/student_home.html'
	
	def post(self,request,*args,**kwargs):
		
		form = BeginReportForm(request.POST)
		
		if form.is_valid():
			student_pk = form.cleaned_data['student_name']
			student = Student.objects.get(pk=student_pk)
			new_report = Report(student=student)
			new_report.save()
			report_pk = new_report.pk
			return redirect('/edit_report/'+str(report_pk)+'/')
			
			
		context = {
			'form':form,
		}
		
		return render(request,self.template,context)
		
	def get(self,request,*args,**kwargs):
		
		form = BeginReportForm()
		
		context = {
			'form':form,
		}
		
		return render(request,self.template,context)		
		
class EditReport(View):
	
	template = 'revenueTracker/edit_report.html'
			
	def get(self,request,*args,**kwargs):
		
		report_pk = kwargs.pop('report_pk')
		report = Report.objects.get(pk=report_pk)
		
		checks = CheckPayment.objects.filter(report=report)
		cash = CashPayment.objects.filter(report=report)
		context = {
			'report':report,
			'checks':checks,
			'cash':cash,
		}
		
		return render(request,self.template,context)
		
def update_report_table(request,report):
	
	template = 'revenueTracker/report_table_update.html'
	
	checks = CheckPayment.objects.filter(report=report)
	cash = CashPayment.objects.filter(report=report)
	context = {
		'report':report,
		'checks':checks,
		'cash':cash,
	}
	
	return render(request,template,context)
	
class AddCheckModal(View):
	
	template = 'revenueTracker/add_cash_modal.html'
	
	def get(self,request,*args,**kwargs):
		
		gift_pk = kwargs.pop('check_pk',False)
		report_pk = kwargs.pop('report_pk')
		student_pk = kwargs.pop('student_pk')
		
		if gift_pk:
			form = AddCheckGiftForm(student_pk=student_pk, report_pk=report_pk, gift_pk=gift_pk)
			
			context = {
				'form':form,
				'gift_pk':gift_pk,
				'report_pk':report_pk,
				'student_pk':student_pk,
			}
			
		else:
			form = AddCheckGiftForm(student_pk=student_pk, report_pk=report_pk)
			
			context= {
				'form':form,
				'report_pk':report_pk,
				'student_pk':student_pk,
			}
			
		return render(request,self.template,context)
		
	def post_logic(self,request,*args,**kwargs):
		
		gift_pk = kwargs.pop('check_pk',False)
		report_pk = kwargs.pop('report_pk')
		student_pk = kwargs.pop('student_pk')
		
		if gift_pk:
			form = AddCheckGiftForm(request.POST, gift_pk=gift_pk, student_pk=student_pk, report_pk=report_pk)
			
		else:
			form = AddCheckGiftForm(request.POST, report_pk=report_pk, student_pk=student_pk)
			
		if form.is_valid():
			data = form.cleaned_data
			report = Report.objects.get(pk=data['report_pk'])
			student = Student.objects.get(pk=data['student_pk'])
			
			if gift_pk:
				
				gift = CheckPayment.objects.get(pk=gift_pk)
				gift.salutation = data['salutation']
				gift.first_name = data['first_name']
				gift.last_name = data['last_name']
				gift.street_address = data['street_address']
				gift.city = data['city']
				gift.state = data['state']
				gift.zip_code = data['zip_code']
				gift.check_number = data['check_number']
				student.update_check(gift,data['amount'])
			
			else:
				
				new_gift = CheckPayment(
					amount = data['amount'],
					salutation = data['salutation'],
					first_name = data['first_name'],
					last_name = data['last_name'],
					street_address = data['street_address'],
					city = data['city'],
					state = data['state'],
					zip_code = data['zip_code'],
					recorded = False,
					report = report,
				)
				student.record_check(new_gift)
				
			return ['redirect',update_report_table(request,report)]
			
		context = {
			'form':form,
		}
		
		return ['context',context]
		
	def post(self,request,*args,**kwargs):
		post_logic_return = self.post_logic(request,*args,**kwargs)
		if post_logic_return[0] == 'context':
			return render(request,self.template,post_logic_return[1])
		if post_logic_return[0] == 'redirect':
			return post_logic_return[1]
			
class AddCashModal(View):
	
	template = 'revenueTracker/add_cash_modal.html'
	
	def get(self,request,*args,**kwargs):
		
		gift_pk = kwargs.pop('cash_pk',False)
		report_pk = kwargs.pop('report_pk')
		student_pk = kwargs.pop('student_pk')
		
		if gift_pk:
			form = AddCashGiftForm(student_pk=student_pk, report_pk=report_pk, gift_pk=gift_pk, initial={'gift_pk':gift_pk,'student_pk':student_pk,'report_pk':report_pk})
			
			context = {
				'form':form,
				'gift_pk':gift_pk,
				'report_pk':report_pk,
				'student_pk':student_pk,
			}
			
		else:
			form = AddCashGiftForm(student_pk=student_pk, report_pk=report_pk, initial={'report_pk':report_pk,'student_pk':student_pk})
			
			context = {
				'form':form,
				'report_pk':report_pk,
				'student_pk':student_pk,
			}
		
		return render(request,self.template,context)
		
	def post_logic(self,request,*args,**kwargs):
		
		gift_pk = kwargs.pop('cash_pk',False)
		report_pk = kwargs.pop('report_pk')
		student_pk = kwargs.pop('student_pk')
		
		if gift_pk:
			form = AddCashGiftForm(request.POST, gift_pk=gift_pk, student_pk=student_pk, report_pk=report_pk)
			
		else:
			form = AddCashGiftForm(request.POST, report_pk=report_pk, student_pk=student_pk)
			
		if form.is_valid():
			data = form.cleaned_data
			report = Report.objects.get(pk=data['report_pk'])
			student = Student.objects.get(pk=data['student_pk'])
			
			if gift_pk:
				
				gift = CashPayment.objects.get(pk=gift_pk)
				gift.salutation = data['salutation']
				gift.first_name = data['first_name']
				gift.last_name = data['last_name']
				gift.street_address = data['street_address']
				gift.city = data['city']
				gift.state = data['state']
				gift.zip_code = data['zip_code']
				student.update_cash(gift,data['amount'])
			
			else:
				new_gift = CashPayment(
					amount = data['amount'],
					salutation = data['salutation'],
					first_name = data['first_name'],
					last_name = data['last_name'],
					street_address = data['street_address'],
					city = data['city'],
					state = data['state'],
					zip_code = data['zip_code'],
					recorded = False,
					report = report
				)
				student.record_cash(new_gift)
				
			return ['redirect',update_report_table(request,report)]
		
		context = {
			'form':form,
		}
		
		return ['context',context]
	
	def post(self,request,*args,**kwargs):
		post_logic_return = self.post_logic(request,*args,**kwargs)
		if post_logic_return[0] == 'context':
			return render(request,self.template,post_logic_return[1])
		if post_logic_return[0] == 'redirect':
			return post_logic_return[1]
	
