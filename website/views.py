

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm , DrugForm, SearchForm,Orderform
from .models import Record,Drug,Order
from django.db.models import Q
from django.db.models import Sum
from django.forms import modelform_factory


from django.contrib.auth.models import User


def home(request):
	records = Record.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records':records})



def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})



def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')

def customer_medication(request):
	records = Record.objects.all()
	medications = Drug.objects.all()
	if request.user.is_authenticated:
		# Look Up Records
		total_sum = Record.objects.aggregate(Sum('price'))['price__sum']
		customer_medications = Drug.objects.all()
		customer_records = Record.objects.all()
		return render(request, 'customer_medication.html', {'records':records ,'medications':medications,'total_sum':total_sum})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')



def delete_record(request, pk):
	if request.user.is_authenticated:
		if request.user.is_staff:
			delete_it = Record.objects.get(id=pk)
			delete_it.delete()
			messages.success(request, "Record Deleted Successfully...")
			return redirect('home')
		else:
			messages.success(request, "access denied, you are not admin user")
			return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')


def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				drug_name = form.cleaned_data['drug_name']
				quantity_sold = form.cleaned_data['quantity_sold']
				drug_find = Drug.objects.get(drug_name=drug_name)
				drug_price = drug_find.price
				form1 = form.save(commit=False)
				form1.price = quantity_sold * drug_price
				drug_purchased = drug_find.quantity_purchased
				drug_name2 = drug_find.drug_name
				if drug_name == drug_name2:
					if drug_purchased != 0:
						add_record = form1.save()
						messages.success(request, "Record Added...")
						total = drug_purchased - quantity_sold
						#form2 = DrugForm(request.POST or None, instance=drug_find)
						MyForm = modelform_factory(Drug, fields=('quantity_purchased',))
						form2 = MyForm(instance=drug_find)
						update_form2 = form2.save(commit=False)
						update_form2.quantity_purchased = total
						update_form2.save()
						messages.success(request, "drug have been updated ")
						messages.success(request,total )
					else:
						messages.success(request, " " + drug_name + " is currenty out of stock  ")

				#else:
					#messages.success(request, " "+drug_name+" is currenty out of stock  ")
					#add_record = form.save()

				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')


def update_record(request, pk):
	if request.user.is_authenticated:
		if request.user.is_staff:
			current_record = Record.objects.get(id=pk)
			form = AddRecordForm(request.POST or None, instance=current_record)
			if form.is_valid():
				if form.is_valid():
					drug_name = form.cleaned_data['drug_name']
					quantity_sold = form.cleaned_data['quantity_sold']
					drug_find = Drug.objects.get(drug_name=drug_name)
					drug_price = drug_find.price
					drug_purchased = drug_find.quantity_purchased
					drug_name2 = drug_find.drug_name
					if drug_name == drug_name2:
						if drug_purchased != 0:
							messages.success(request, "Record Added...")
							old_drug = current_record.quantity_sold
							if quantity_sold <= drug_purchased :
								total = drug_purchased - old_drug + quantity_sold
								total2 = drug_price * quantity_sold

							# form2 = DrugForm(request.POST or None, instance=drug_find)
							MyForm = modelform_factory(Drug, fields=('quantity_purchased',))
							form2 = MyForm(instance=drug_find)
							update_form2 = form2.save(commit=False)
							update_form2.quantity_purchased = total
							update_form2.save()
							form1 = form.save(commit=False)
							form1.price = total2
							form1.save()
							messages.success(request, "drug have been updated ")
							messages.success(request, total)
						else:
							messages.success(request, " " + drug_name + " is currenty out of stock  ")
				return redirect('home')
			return render(request, 'update_record.html', {'form':form})
		else:
			messages.success(request, "access denied , you are not admin...")
			return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')


def index(request):
    # Get the logged-in user's ID
    user_id = request.user.username

    # Pass the user ID to the template
    return render(request, 'home.html', {'user_id':user_id})

def medication(request):
	form = DrugForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				medication = form.save()
				return redirect('home')
		return render(request, 'medication.html', {'form':form})

	else:
		messages.success(request, "you aer not logged in ")
		return  redirect('home')

def view_medication(request , pk):
	if request.user.is_authenticated:
		customer_medication = medication.objects.get(id=pk)

		return render(request, 'record.html', {'customer_medication': customer_medication})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')



'''def search_records(request):
	form = SearchForm(request.GET)
	if form.is_valid():
		query = form.cleaned_data['query']
		records = Record.objects.filter(title__icontains=query)
	else:
		records = Record.objects.all()

	context = {'form': form, 'records': records}
	return render(request, 'home.html', context)  '''
def search(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			searched = request.POST['searched']
			records= Record.objects.filter(customer_name__contains=searched)

			return render(request,'search.html',{'searched':searched ,'records':records})
		else:
			return render(request,'search.html')
	else:
		messages.success(request, "you aer not logged in ")
		return  redirect('home')

def sold_drug(request):

	sales = Record.objects.all()
	if request.user.is_authenticated:
		return render(request, 'avaliable_drugs.html', {'sales': sales})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')


def update_drug(request, pk):
	if request.user.is_authenticated:
		if request.user.is_staff:
			current_drug = Drug.objects.get(id=pk)
			form = DrugForm(request.POST or None, instance=current_drug)
			if form.is_valid():
				form.save()
				messages.success(request, "Invertory Has Been Updated!")
				return redirect('home')
			return render(request, 'update_drug.html', {'form':form})
		else:
			messages.success(request, "access denied , you are not admin...")
			return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

#deleting a drug from the system
def delete_drug(request, pk):
	if request.user.is_authenticated:
		if request.user.is_staff:
			delete_it = Drug.objects.get(id=pk)
			delete_it.delete()
			messages.success(request, "Record Deleted Successfully...")
			return redirect('home')
		else:
			messages.success(request, "access denied, you are not admin user")
			return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')
#list all the drugs in the drugs table
def view_drugs(request):
	avaliables= Drug.objects.all()
	if request.user.is_authenticated:
		return render(request, 'drug.html',{'avaliables':avaliables})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
#view individual records for the drugs
def view_drug_record(request ,pk):
	if request.user.is_authenticated:
		drug_record = Drug.objects.get(id=pk)

		return render(request, 'drug_record.html', {'drug_record': drug_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')