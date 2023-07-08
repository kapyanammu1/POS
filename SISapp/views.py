from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category, Customer, Order, Order_Item, Sale
from .forms import Items, Categories, Customers, Orders, DisabledOrders, SignupForm
from datetime import datetime, timedelta
from django.db.models import Sum, F, Value, DecimalField
from django.db.models.functions import TruncDate, TruncMonth, Coalesce
from django.http import JsonResponse
from django.contrib.auth import logout
# Create your views here.

@login_required
def index(request):
    today = datetime.now()
    day_Before = today-timedelta(days=1)
    thisMonth = datetime.now().month
    month_Before = datetime.now().date().replace(day=1) - timedelta(days=1)
    thisYear = datetime.now().year
    paid_orders =  Order.objects.exclude(sale__isnull=True)
    paid_items_filtered = Order_Item.objects.exclude(order__isnull=True)
    total_quantity = paid_items_filtered.filter(order__sale__sale_time__date=today).aggregate(total_quantity=Sum('quantity'))['total_quantity']
    #total_quantity1 = paid_items_filtered.filter(order__sale__sale_time__date=day_Before).aggregate(total_quantity1=Coalesce(Sum('quantity', output_field1=DecimalField()), Value(0, output_field1=DecimalField())))['total_quantity1']
    total_quantity1 = paid_items_filtered.filter(order__sale__sale_time__date=day_Before).aggregate(total_quantity1=Sum('quantity'))['total_quantity1']
    total_sales = Sale.objects.filter(sale_time__month=thisMonth).aggregate(total_sales=Sum('total_amount'))['total_sales']  
    total_sales1 = Sale.objects.filter(sale_time__month=month_Before.month).aggregate(total_sales1=Coalesce(Sum('total_amount', output_field=DecimalField()), Value(0, output_field=DecimalField())))['total_sales1']
    items = Item.objects.all()
    customer = Order.objects.filter(order_time__year=thisYear).count()  
    customer1 = Order.objects.filter(order_time__year=thisYear-1).count()
    total_sales = total_sales or 0
    total_sales1 = total_sales1 or 0
    total_quantity = total_quantity or 0
    total_quantity1 = total_quantity1 or 0
    if customer1 != 0:
         Customer_percent = int(((customer - customer1)/customer1) * 100)
    else:
         Customer_percent = 0

    if (Customer_percent < 0):
        Customer_percent = abs(Customer_percent)
        option2 = "decrease"
    else:
        option2 = "increase"   

    if total_sales1 != 0 :
         Sales_percent = int(((total_sales - total_sales1)/total_sales1) * 100)
    else:
         Sales_percent = 0
   
    if (Sales_percent < 0):
        Sales_percent = abs(Sales_percent)
        option1 = "decrease"
    else:
        option1 = "increase" 


    if total_quantity1 != 0:
        ItemSold_percent = int(((total_quantity - total_quantity1)/total_quantity1) * 100)
    else:
        ItemSold_percent = 0

    if (ItemSold_percent < 0):
        ItemSold_percent = abs(ItemSold_percent)
        option = "decrease"
    else:
        option = "increase"

    salesToday = Order_Item.objects.filter(order__sale__sale_time__date=today).values('item__name').annotate(total_quantity=Sum('quantity'), total_price=F('item__price') * Sum(F('quantity')))
    salesthisMonth = Sale.objects.filter(sale_time__month=thisMonth).annotate(sale_date=TruncDate('sale_time')).values('sale_date').annotate(total_sales=Sum('total_amount')).order_by('sale_date').distinct()
    salesthisYear = Sale.objects.filter(sale_time__year=thisYear).annotate(sale_date=TruncMonth('sale_time')).values('sale_date').annotate(total_sales=Sum('total_amount')).order_by('sale_date').distinct()
    
    barChart_thisMonth = Order_Item.objects.filter(order__sale__sale_time__month=thisMonth).values('item__name').annotate(total_quantity=Sum('quantity'), total_price=F('item__price') * Sum(F('quantity')))
    barChart_thisYear = Order_Item.objects.filter(order__sale__sale_time__year=thisYear).values('item__name').annotate(total_quantity=Sum('quantity'), total_price=F('item__price') * Sum(F('quantity')))
    total_qty_per_item = Order_Item.objects.values('item__name').annotate(total_quantity=Sum('quantity'), total_price=F('item__price') * Sum(F('quantity'))).order_by('-total_price')

    context = {
        'total_quantity': total_quantity,
        'total_sales': total_sales,
        'paid_orders': paid_orders,
        'items': items,
        'customer': customer,
        'salesToday': salesToday,
        'salesthisMonth': salesthisMonth,
        'salesthisYear': salesthisYear,
        'ItemSold_percent': ItemSold_percent,
        'Sales_percent': Sales_percent,
        'Customer_percent': Customer_percent,
        'option': option,
        'option1': option1,
        'option2': option2,
        'barChart_thisMonth': barChart_thisMonth,
        'barChart_thisYear': barChart_thisYear,
        'total_qty_per_item' : total_qty_per_item,
    }
    return render(request, 'index.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def tables_data(request):
    items = Item.objects.all()
    return render(request, 'tables-data.html', {'items': items})

@login_required
def AddItem(request):
    if request.method == 'POST':
        form = Items(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tables_data')
    else:
        form = Items()
    return render(request, 'AddItems.html', {'form': form})

@login_required
def EditItems(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = Items(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('tables_data')
    else:
        form = Items(instance=item)
    return render(request, 'EditItems.html', {'form': form, 'item': item})

@login_required
def deleteItems(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('tables_data')
    return render(request, 'deleteItems.html', {'item': item})

@login_required
def deleteSales(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('Sales')
    return render(request, 'deleteSales.html', {'sale': sale})

@login_required
def CategoryForm(request):
    category =  Category.objects.all()
    return render(request, 'CategoryForm.html', {'category': category})

@login_required
def CustomerForm(request):
    customer =  Customer.objects.all()
    return render(request, 'CustomerForm.html', {'customer': customer})

@login_required
def AddCustomer(request):
    if request.method == 'POST':
        form = Customers(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('CustomerForm')
    else:
        form = Customers()
    return render(request, 'AddCustomer.html', {'form': form})

@login_required
def EditCustomer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = Customers(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('CustomerForm')
    else:
        form = Customers(instance=customer)
    return render(request, 'EditCustomer.html', {'form': form, 'customer': customer})

@login_required
def deleteCustomer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('CustomerForm')
    return render(request, 'deleteCustomer.html', {'customer': customer})

@login_required
def AddCategory(request):
    if request.method == 'POST':
        form = Categories(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('CategoryForm')
    else:
        form = Categories()
    return render(request, 'AddCategory.html', {'form': form})

@login_required
def deleteCategory(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('CategoryForm')
    return render(request, 'deleteCategory.html', {'category': category})

@login_required
def deleteOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('Order_ListForm')
    return render(request, 'deleteCategory.html', {'order': order})

@login_required
def DeleteOrder_Items(request, pk):
    order_item = get_object_or_404(Order_Item, pk=pk)
    if request.method == 'POST':
        order_item.delete()
        return redirect('Order_Items')
    return render(request, 'Order_Items.html', {'order_item': order_item})

@login_required
def EditCategory(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = Categories(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('CategoryForm')
    else:
        form = Categories(instance=category)
    return render(request, 'EditCategory.html', {'form': form, 'category': category})

@login_required
def OrderForm(request):
    itemOb = Item.objects.all()
    if request.method == 'POST':
        order_form = Orders(request.POST, request.FILES)

        if order_form.is_valid():
            order = order_form.save()  # Save the Order instance
            order_items = request.POST.getlist('order_items')

            for item in order_items:
                name, quantity = item.split(',')

                order_item = Order_Item()
                order_item.order = order
                order_item.item = Item.objects.get(name=name)
                order_item.quantity = quantity
                order_item.save()
            return redirect('Order_ListForm')

    else:
        order_form = Orders()
    context = {
        'order_form': order_form,
        'itemOb': itemOb,
    }
    return render(request, 'OrderForm.html', context)

@login_required
def Edit_Order(request, pk):
    order_pk = get_object_or_404(Order, pk=pk)
    items_filtered = Order_Item.objects.select_related('order', 'item').filter(order=order_pk)
    itemOb = Item.objects.all()
    if request.method == 'POST':
        order_form = Orders(request.POST, request.FILES, instance=order_pk)
        if order_form.is_valid():
            order = order_form.save()  # Save the Order instance
            order_items = request.POST.getlist('order_items')
            order.order_items.all().delete()
            for item in order_items:
                name, quantity = item.split(',')
                order_item = Order_Item()
                order_item.order = order
                order_item.item = Item.objects.get(name=name)
                order_item.quantity = quantity
                order_item.save()
            return redirect('Order_ListForm')
    else:
        sumaTotal = 0
        order_form = Orders(instance=order_pk)
        for order_item in items_filtered:
            order_item.total_price = order_item.quantity * order_item.item.price
            sumaTotal += order_item.total_price
            #order_item.totalPrice = sum([x.total_price for x in items_filtered])
    context = {
        'order_form': order_form,
        'itemOb': itemOb,
        'items_filtered': items_filtered,
        'sumaTotal': sumaTotal,
    }
    return render(request, 'EditOrder.html', context)

@login_required
def Payment(request, pk):
    sumaTotal = 0
    order_pk = get_object_or_404(Order, pk=pk)
    items_filtered = Order_Item.objects.select_related('order', 'item').filter(order=order_pk)
    if request.method == 'POST':
        order_form = Orders(request.POST, request.FILES, instance=order_pk)
        #payment = Sales(request.POST, request.FILES)       
        if order_form.is_valid():
            total_amount = request.POST.get('total_amount')
            try:
                total_amount = float(total_amount)
                if total_amount > 0:
                    order = order_form.save()            
                    payment = Sale()
                    payment.order = order
                    payment.total_amount = total_amount
                    payment.save()           
                    return redirect('Order_ListForm')   
                else:
                    pass
            except ValueError:
                pass               
    else:              
        order_form = Orders(instance=order_pk)
        order_form_display = DisabledOrders(instance=order_pk)       
        for order_item in items_filtered:
            order_item.total_price = order_item.quantity * order_item.item.price
            sumaTotal += order_item.total_price
            #order_item.totalPrice = sum([x.total_price for x in items_filtered])
    context = {
        'order_form': order_form,
        'items_filtered': items_filtered,
        'sumaTotal': sumaTotal,
        'order_form_display': order_form_display,
    }
    return render(request, 'Payment.html', context)

@login_required
def Order_ListForm(request):
    order = Order.objects.exclude(sale__isnull=False)    
    return render(request, 'Order_ListForm.html', {'order': order})

@login_required
def SalesForm(request):
    sales = Sale.objects.all().order_by('-sale_time')    
    order = Order.objects.all()
    order_item = Order_Item.objects.all()
    items = Item.objects.all()
    return render(request, 'Sales.html', {'sales': sales, 'order': order, 'order_item': order_item, 'items': items})
    
@login_required
def Order_Items(request, pk):    
    order = get_object_or_404(Order, pk=pk)
    #filtred_Order = order.order_items.all()
    order_items = Order_Item.objects.select_related('order', 'item').filter(order=order)
    if request.method == 'POST':
        order_item = get_object_or_404(Order_Item, pk=order_item.pk)
        order_item.delete()
    return render(request, 'Order_Items.html', {'order_items': order_items})

@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

@login_required
def get_order_items(request):
    sale_id = request.GET.get('sale_id')
    
    try:
        sale = Sale.objects.get(pk=sale_id)
        orders = Order.objects.filter(sale=sale)
        order_items = Order_Item.objects.filter(order__in=orders)
        items = Item.objects.all()
        
        # Prepare the order items data as a list of dictionaries
        order_items_data = []
        for order_item in order_items:
            item = items.filter(pk=order_item.item.pk).first()  # Retrieve the item from the queryset
            if item:
                order_items_data.append({
                    'name': item.name,
                    'qty': order_item.quantity,
                    'price': item.price,
                })
        
        return JsonResponse({'order_items': order_items_data,} )
    
    except Sale.DoesNotExist:
        return JsonResponse({'order_items': []})

