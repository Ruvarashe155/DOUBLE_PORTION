from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from . models import *
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from datetime import date










def login_user(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                raise ValueError("Username and password are required.")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Login successful'})
            else:
                return JsonResponse({'success': False, 'message': 'Incorrect username or password'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred during login.', 'error': str(e)})
        
    return render(request, 'login.html')


def logoutuser(request):
    return render(request, 'login.html')

@login_required
def staff(request):
    if request.method=='POST':
        name=request.POST.get('name')
        id=request.POST.get('id')
        last_staff = users.objects.order_by('-user_id').first()
        if last_staff:
            last_staff_number = int(last_staff.user_id[3:])
            new_staff_number = last_staff_number + 1
        else:
                new_staff_number = 1

        staff_no = f"USR{new_staff_number:03}"
        

        save_staff = users(full_name=name,user_id=staff_no)
        save_staff.save()
    context ={
        'staff_list': users.objects.all()
    }

    return render(request, 'staff.html', context)

@login_required
def products(request):
    if request.method=='POST':
        product_name=request.POST.get('product_name')
        # description=request.POST.get('description')
        units=request.POST.get('units')
        # cost=request.POST.get('cost')

        last_product = our_product.objects.order_by('-product_id').first()
        if last_product:
            last_product_number = int(last_product.product_id[3:])
            new_product_number = last_product_number + 1
        else:
                new_product_number = 1

        product_id = f"PDT{new_product_number:03}"
        save_product = our_product( product_id=product_id,product_name=product_name,units=units, )
        save_product.save()
    context ={
        'product_list': our_product.objects.all().order_by('-product_id')
    }

    return render(request, 'products.html', context)


def products_var(request):
    if request.method=='POST':
        product_name=request.POST.get('product_name')
        unit_size=request.POST.get('unit_size')
        units=request.POST.get('units')

        product_name=our_product.objects.get(product_id=product_name)
        

        last_product = product_variant.objects.order_by('-product_var_id').first()
        if last_product:
            last_product_number = int(last_product.product_var_id[3:])
            new_product_number = last_product_number + 1
        else:
                new_product_number = 1

        product_id = f"PDV{new_product_number:03}"
        save_product = product_variant( product_var_id=product_id,product=product_name,unit=units,unit_size=unit_size )
        save_product.save()
    context ={
        'product_list': our_product.objects.all(),
        'products':product_variant.objects.all()
    }

    return render(request, 'product_variant.html', context)


@login_required
def manufactured_product(request):
    if request.method=='POST':
        products_name=request.POST.get('product_name')
        quantity=request.POST.get('quantity')
        description=request.POST.get('description')
        date = request.POST.get('date')
        total = request.POST.get('cost')

        products_name=our_product.objects.get(product_id=products_name)
    
        last_stock_product = stock.objects.order_by('-stock_id').first()
        if last_stock_product:
            last_product_number = int(last_stock_product.stock_id[3:])
            new_product_number = last_product_number + 1
        else:
            new_product_number = 1

        stock_id = f"STK{new_product_number:03}"
        last_manufactured_products = manufactured_products.objects.order_by('-m_id').first()
        if last_manufactured_products:
            last_product_number = int(last_manufactured_products.m_id[3:])
            new_products_number = last_product_number + 1
        else:
                new_products_number = 1

        m_id = f"MND{new_products_number:03}"

        total =0
        total+= int(quantity)
        products_manufactured = manufactured_products(m_id=m_id,product=products_name,quantity=quantity,description=description,date=date, total=total)
        products_manufactured.save()
          
        manufactured=manufactured_products.objects.get(m_id=m_id)
        save_stock = stock(stock_id=stock_id, product_id=manufactured ,quantity=quantity)
        save_stock.save()

    context= {'product':our_product.objects.all(),
              'manufactured_product_list': manufactured_products.objects.all().order_by('-m_id')
              }
    return render(request, 'manufactured_products.html', context)


@login_required
def packing_product(request):
    if request.method=='POST':
        products_name=request.POST.get('product_name')
        quantity=request.POST.get('quantity')
        date = request.POST.get('date')
        units=request.POST.get('units')
        unit_size=request.POST.get('unit_size')


        last_packed_products = packing.objects.order_by('-pack_id').first()
        if last_packed_products:
            last_product_number = int(last_packed_products.pack_id[3:])
            new_products_number = last_product_number + 1
        else:
                new_products_number = 1
    
        product=product_variant.objects.get(product_var_id=products_name)
        pack_id = f"PCK{new_products_number:03}"
        products_packed = packing(pack_id=pack_id,quantity=quantity,date=date,unit=units,unit_size=unit_size,product=product)
        products_packed.save()
        
        
           

    context= {'product':product_variant.objects.all(),
              'packed_product_list': packing.objects.all().order_by('-pack_id'),
              
              }
    return render(request, 'packing.html', context)



from django.db.models import Sum, F
@login_required
def sales_report(request):
    sale=sales.objects.all()
    date_filter=request.GET.get('datefilter')
    product_filter=request.GET.get('productfilter')
    seller_filter=request.GET.get('sellerfilter')
    
        

    if date_filter:
        sale=sales.objects.filter(date=date_filter).all()
    elif product_filter:
        sale=sales.objects.filter(product=product_filter)  
    elif seller_filter:
        sale=sales.objects.filter(user=seller_filter) 
    elif date_filter and product_filter:
        sale = sales.objects.filter(date=date_filter,product=product_filter )       
    else:
        sale=sales.objects.all()


    if request.method=='POST':
        product_name=request.POST.get('product_name')
        quantity=float(request.POST.get('quantity'))
        description=request.POST.get('description')
        # return HttpResponse(product_name)
        date = request.POST.get('date')
        cost = request.POST.get('cost')
        status=request.POST.get('status')
        user = request.POST.get('user')

        
        total_cost= float(cost)* float(quantity)
        product_name=product_variant.objects.get(product_var_id=product_name)
        
        user = users.objects.get(user_id=user)
        remaining_stock=user.get_remaining(product_name)

        if remaining_stock <=0:
            messages.error(request, "You have no allocated stock remaining for this product")

        elif quantity > remaining_stock:
            messages.error(request, f"You only have {remaining_stock} units remaining") 
        else:       

            product_sales = sales(product=product_name,quantity=quantity,description=description,date=date,cost=cost,total_cost=total_cost, user=user,status=status)
            product_sales.save()
            messages.success(request, "Sale recorded successfully")

    cash_sales=sales.objects.filter(status='cash').aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    credit_paid=credit_payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    credit_sales=sales.objects.filter(status='credit').aggregate(Sum('total_cost'))['total_cost__sum'] or 0

    total_credit_sales=credit_sales-credit_paid
    total_cash_sales=cash_sales+credit_paid

    
    context= {'product':product_variant.objects.all(),
            #   'sales_list':sales.objects.all().order_by('-id'),
            'sales_list':sale.order_by('-id'),
              'user_list':users.objects.all(),
              'total_cash_sales':total_cash_sales,
              'total_credit_sales':total_credit_sales,
              
              }
    
    return render(request, 'sales.html', context)


@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect('records:login')
    
    context={
        'total_products':our_product.objects.count(),
        'total_allocated':allocation.objects.count(),
        'total_sales':sales.objects.count(),
        

    }
    return render(request, 'home.html', context)


@login_required
def stocking(request):
    manu =manufactured_products.objects.all()
    stockk = stock.objects.all()
    context = {
          'stock_list':inventory.objects.all(),
          'sales_list':sales.objects.all()
          
     }
    return render(request, 'stock_list.html' , context)



@login_required
def allocating(request):
    allocations=allocation.objects.all()
    date_filter=request.GET.get('datefilter')
    product_filter=request.GET.get('productfilter')
    seller_filter=request.GET.get('sellerfilter')
    # return HttpResponse(product_filter)
    
    
        

    if date_filter:
        allocations=allocation.objects.filter(date=date_filter).all()
    elif product_filter:
        # allocations=allocation.objects.filter(pack_id__product=product_filter)  
        allocations=allocation.objects.filter(pack_id=packing.objects.filter(product=product_variant.objects.filter(product_var_id=product_filter).first()).first())
    elif seller_filter:
        allocations=allocation.objects.filter(user_id=seller_filter)    
    else:
        allocations=allocation.objects.all()


    if request.method=='POST':
        user = request.POST.get('name')
        product = request.POST.get('product')
        # return HttpResponse(product)
        date = request.POST.get('date')
        quantity = int(request.POST.get('quantity'))
        unit_size=request.POST.get('unit_size')
        units = request.POST.get('units')
        cost = request.POST.get('cost')

        total_cost= float(cost)* float(quantity)

        user = users.objects.get(user_id=user)
        allo = packing.objects.filter(product=product_variant.objects.get(product_var_id=product)).first()

        product = packing.objects.filter(product=product_variant.objects.get(product_var_id=product)).first()

        products=product.product
        available_stock=products.current_stock()

        
        
        if quantity > available_stock:
             messages.error(request, "Allocation failed: Not enough stock available !!")
        else:    
            allo = allocation(pack_id=allo, user_id=user, date=date,quantity=quantity, units=units, unit_size=unit_size,cost=cost, total_cost=total_cost )
            allo.save()
            messages.success(request, "Product allocated successfully")

        stock_product =stock.objects.all()
        for stockk in stock_product:
             
            stockk.col_allo_stat="ALLOCATED"
            stockk.save()

    total_expected=allocation.objects.filter(user_id=seller_filter).aggregate(Sum('total_cost'))['total_cost__sum'] or 0
 
    context = {
        'name_list':users.objects.all(),
        'product_list':manufactured_products.objects.all(),
        #   'allocation_list':allocation.objects.all().order_by('-id'),
        'allocation_list':allocations.order_by('-id'),
        'products':product_variant.objects.all(),
        'sellers':users.objects.all(),
        'expected_total': total_expected,

    }
    return render(request, 'allocation.html', context)



@login_required
def curr(request):
    return render(request, 'currency.html')

@login_required
def product_list(request):
    products=our_product.objects.all()
    context= {
        'products':products
    }
    return render(request, 'stock.html' ,context)

@login_required
def packed_stock(request):
    products=product_variant.objects.all()
    context= {
        'products':products
    }
    return render(request, 'packed_stock.html' ,context)




@login_required
def user_stock_report(request):
    users_list = users.objects.all()
    products_list =product_variant.objects.all()

    report = []
    for user in users_list:
        for product in products_list:
            allocated= user.get_allocated(product)
            sold =user.get_sold(product)
            remaining =user.get_remaining(product)
            if allocated>0 or sold>0:
                stock=user_stock_record(user=user.full_name, product=product.product.product_name,unit_size= product.unit_size,unit=product.unit,allocated=allocated, sold=sold, remaining=remaining,date=date.today())
                stock.save()
                report.append({'user':user.full_name, 'product':product.product.product_name,'unit_size': product.unit_size,'units':product.unit, 'allocated':allocated, 'sold':sold, 'remaining':remaining})
    return render(request, 'user_stock.html', {'report':report})


@login_required
def expenses(request):
    if request.method=='POST':
        date=request.POST.get('date')
        description=request.POST.get('description')
        amount=float(request.POST.get('amount'))
        category=request.POST.get('category')
        budgeting = request.POST.get('budget')
        id=request.POST.get('id')
        # return HttpResponse(id)

        last_expense = expense.objects.order_by('-expense_id').first()
        if last_expense:
            last_number = int(last_expense.expense_id[3:])
            new_number = last_number + 1
        else:
                new_number = 1

        expense_id = f"EXP{new_number:03}"
        budgeting = budget.objects.get(budget_id=budgeting)
        category = expense_category.objects.get(id=category)
        
        # if id:
        #     existing_exp_entry=expense.objects.filter(id=id).first()
        #     if existing_exp_entry:
            
        #         existing_exp_entry.date=date
        #         existing_exp_entry.amount=amount
        #         existing_exp_entry.description=description
        #         existing_exp_entry.budget=budgeting
        #         existing_exp_entry.category=category
        #         existing_exp_entry.save()
        #     else:
        remaining=budgeting.remaining()
        if amount > remaining:
            messages.error(request, f"Budget left is ${remaining}")
        elif remaining <=0:
            messages.error(request, f"Remaining Budget is ${remaining}")
        else:        
            save_expense = expense( expense_id=expense_id,date=date,category=category,description=description,amount=amount, budget=budgeting)
            save_expense.save()
            messages.success(request, "Expense successfully saved")
    context ={
        'expense_list': expense.objects.all().order_by('-id'),
        'budget_list':budget.objects.all(),
        'category_list': expense_category.objects.all(),
    }

    return render(request, 'expense.html', context)


@login_required
def budgeting(request):
    if request.method=='POST':
        month=request.POST.get('month')
        amount=request.POST.get('amount')
        id=request.POST.get('id')
       
       

        last_budget = budget.objects.order_by('-budget_id').first()
        if last_budget:
            last_number = int(last_budget.budget_id[3:])
            new_number = last_number + 1
        else:
                new_number = 1
        if id:
            existing_bud_entry=budget.objects.get(budget_id=id)
            existing_bud_entry.month=month
            existing_bud_entry.amount=amount
            existing_bud_entry.save()
        else:
            budget_id = f"BUD{new_number:03}"
            save_budget = budget( budget_id=budget_id,month=month,amount=amount)
            save_budget.save()
        


    context ={
        
        'budget_list':budget.objects.all()
    }

    return render(request, 'budget.html', context)

@login_required
def category(request):
    if request.method=='POST':
        name=request.POST.get('name')
        

        save_category = expense_category(name=name)
        save_category.save()
    context ={
        'category_list': expense_category.objects.all()
    }

    return render(request, 'category.html', context)
@login_required
def budget_report(request):
    bud=budget.objects.all()
    report =[]

    for b in bud:
        report.append({'month':b.month, 'budget':b.amount, 'spent':b.total_expenses, 'remaining':b.remaining, 'usage':b.usage_percentage})
    return render(request ,'budget_report.html', {'report':report})   

@login_required
def credit_payments(request):
    if request.method=='POST':
        date=request.POST.get('date')
        user=request.POST.get('user')  
        amount=request.POST.get('amount')

        user =users.objects.filter(user_id=user).first()
        credits=credit_payment(date=date, user=user, amount=amount) 
        credits.save()
    return render(request, 'credit_payments.html', {'sellers':users.objects.all(), 'credits':credit_payment.objects.all()})    


def cashier(request):
    if request.method=='POST':
        date =request.POST.get('date')
        source =request.POST.get('source')
        type =request.POST.get('type')
        amount =request.POST.get('amount')
        description =request.POST.get('description')
        # return HttpResponse(source)

        seller=users.objects.get(user_id=source)

        report=cashier_report(date=date, source=seller, type=type, amount=amount, description=description)
        report.save()
        messages.success(request,'Transaction successfully saved')
    transactions=cashier_report.objects.all()
    total_received= transactions.filter(type='RECEIVE').aggregate(Sum('amount'))['amount__sum'] or 0
    total_released= transactions.filter(type='RELEASE').aggregate(Sum('amount'))['amount__sum'] or 0
    balance=total_received-total_released
    context={
        'sellers':users.objects.all(),
        'types':cashier_report.TransactionType.choices,
        'cashier_list':cashier_report.objects.all(),
        'received':total_received,
        'released':total_released,
        'balance':balance
    }

    return render(request, 'cashier_report.html', context)    
        


# records/views.py
  # we'll separate ML code here for cleanliness

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ml_utils import predict_stock  # Machine Learning utility

@csrf_exempt
def predict_remaining_view(request):
    if request.method == 'GET':
        try:
            # Extract parameters from GET request
            user = request.GET.get('user')
            product = request.GET.get('product')
            unit_size = float(request.GET.get('unit_size'))
            allocated = float(request.GET.get('allocated'))
            sold = float(request.GET.get('sold'))

            # Validate input
            if not all([user, product]):
                return JsonResponse({'error': 'Missing user or product name'}, status=400)

            # Call ML model for prediction
            prediction = predict_stock(user, product, unit_size, allocated, sold)

            return JsonResponse({'predicted_remaining': prediction})

        except ValueError:
            return JsonResponse({'error': 'unit_size, allocated, and sold must be numbers'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method allowed'}, status=405)






def stock_prediction_page(request):
    user_list = users.objects.all()
    products = product_variant.objects.all()

    context = {
        'user_list': user_list,
        'products': products,
    }
    return render(request, 'predict.html', context)
