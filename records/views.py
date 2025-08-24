from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from . models import *
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages






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
        description=request.POST.get('description')
        units=request.POST.get('units')
        cost=request.POST.get('cost')

        last_product = our_product.objects.order_by('-product_id').first()
        if last_product:
            last_product_number = int(last_product.product_id[3:])
            new_product_number = last_product_number + 1
        else:
                new_product_number = 1

        product_id = f"PDT{new_product_number:03}"
        save_product = our_product( product_id=product_id,product_name=product_name,description=description,units=units, cost=cost)
        save_product.save()
    context ={
        'product_list': our_product.objects.all().order_by('-product_id')
    }

    return render(request, 'products.html', context)

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
from django.db.models import Sum, F
@login_required
def sales_report(request):
    if request.method=='POST':
        product_name=request.POST.get('product_name')
        quantity=float(request.POST.get('quantity'))
        description=request.POST.get('description')
        date = request.POST.get('date')
        cost = request.POST.get('cost')
        status=request.POST.get('status')
        user = request.POST.get('user')

        
        total_cost= float(cost)* float(quantity)
        product_name=our_product.objects.get(product_id=product_name)
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

    
    context= {'product':our_product.objects.all(),
              'sales_list':sales.objects.all().order_by('-id'),
              'user_list':users.objects.all(),
              'total_cash_sales':total_cash_sales,
              'total_credit_sales':total_credit_sales
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
    if request.method=='POST':
        user = request.POST.get('name')
        product = request.POST.get('product')
        date = request.POST.get('date')
        quantity = int(request.POST.get('quantity'))
        units = request.POST.get('units')

        user = users.objects.get(user_id=user)
        product = manufactured_products.objects.get(product=product)

        products=product.product
        available_stock=products.current_stock()
        
        if quantity > available_stock:
            messages.error(request, "Allocation failed: Not enough stock available !!")
        else:    
            allo = allocation(man_id=product, user_id=user, date=date,quantity=quantity, units=units )
            allo.save()
            messages.success(request, "Product allocated successfully")

        stock_product =stock.objects.all()
        for stockk in stock_product:
             
            stockk.col_allo_stat="ALLOCATED"
            stockk.save()

    context = {
          'name_list':users.objects.all(),
          'product_list':manufactured_products.objects.all(),
          'allocation_list':allocation.objects.all().order_by('-id'),
          'products':our_product.objects.all()

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
def user_stock_report(request):
    users_list = users.objects.all()
    products_list =our_product.objects.all()

    report = []
    for user in users_list:
        for product in products_list:
            allocated= user.get_allocated(product)
            sold =user.get_sold(product)
            remaining =user.get_remaining(product)
            if allocated>0 or sold>0:
                report.append({'user':user.full_name, 'product':product.product_name,'units':product.units, 'allocated':allocated, 'sold':sold, 'remaining':remaining})
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



