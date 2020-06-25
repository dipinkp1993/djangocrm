from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from  .forms import *
from .filters import OrderFilter
from django.core.paginator import Paginator
# Create your views here.

def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()
	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	context = {'orders': orders, 'customers': customers,'total_orders':total_orders,'delivered':delivered,
	'pending':pending}
	return render(request, 'accounts/dashboard.html',context)

def products(request):
	products = Product.objects.all()
	paginator = Paginator(products, 2)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'accounts/products.html',{'page_obj': page_obj})

def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()
	myFilter=OrderFilter(request.GET,queryset=orders)
	orders=myFilter.qs
	context = {'customer': customer, 'orders': orders, 'order_count': order_count,'myFilter':myFilter}
	return render(request, 'accounts/customers.html', context)


def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'formset':formset}
	return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/update_form.html', context)

def deleteOrder(request):

	if request.method == "POST":
		data = request.POST.copy()
		oid=data.get('oid')
		order = Order.objects.get(id=oid)
		order.delete()
		return redirect('/')
	else:
		return redirect('/')


