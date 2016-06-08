from __future__ import unicode_literals

from django.db import models


class Student(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	total_raised = models.IntegerField(default=0)
	goal = models.IntegerField(default=1500)
	cash_raised = models.IntegerField(default=0)
	checks_raised = models.IntegerField(default=0)
	
	def record_check(self,check):
		self.checks_raised += check.amount
		self.total_raised += check.amount
		check.recorded = True
		self.save()
		check.save()
		
	def record_cash(self,cash):
		self.cash_raised += cash.amount
		self.total_raised += cash.amount
		cash.recorded = True
		self.save()
		cash.save()
		
	def update_check(self,check, new_amount):
		self.checks_raised -= check.amount
		self.total_raised -= check.amount
		self.checks_raised += new_amount
		self.total_raised += new_amount
		check.amount = new_amount
		check.save()
		self.save()
		
	def update_cash(self,check,new_amount):
		self.cash_raised -= cash.amount
		self.total_raised -= cash.amount
		self.cash_raised += new_amount
		self.total_raised += new_amount
		cash.amount = new_amount
		cash.save()
		self.save()

	def __str__(self):
		return self.first_name + ' ' + self.last_name
	
class Report(models.Model):
	student = models.ForeignKey(Student)
	date = models.DateField(auto_now_add=True)
	submitted = models.BooleanField(default=False)
	approved = models.BooleanField(default=False)
	
	def submit(self):
		self.submitted = True
		self.save()
		
	def approve(self):
		self.approved = True
		self.save()
		
			
class Payment(models.Model):
	amount = models.IntegerField()
	salutation = models.CharField(max_length=10,null=True,blank=True)
	first_name = models.CharField(max_length=20,null=True,blank=True)
	last_name = models.CharField(max_length=20)
	street_address = models.CharField(max_length=40,null=True,blank=True)
	city = models.CharField(max_length=40,null=True,blank=True)
	state = models.CharField(max_length=2,null=True,blank=True)
	zip_code = models.CharField(max_length=10,null=True,blank=True)
	recorded = models.BooleanField(default=False)
	report = models.ForeignKey(Report)
	
class CheckPayment(Payment):		
	check_number = models.CharField(max_length=20,blank=True,null=True)
	
class CashPayment(Payment):
	def __init__(self,*args,**kwargs):
		super (CashPayment,self).__init__(*args,**kwargs)
	

