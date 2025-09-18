from django.db import models
from django.utils import timezone
from django.db.models import Sum, F

# Create your models here.
class users(models.Model):
    user_id = models.CharField(max_length=200, primary_key=True)
    full_name= models.CharField(max_length=200)
    def str(self):
        return f"{self.full_name} ({self.user_id})"

    def get_allocated(self,product):
        return sum(a.quantity for a in allocation.objects.filter(user_id=self, pack_id= packing.objects.filter(product=product).first()) )
    
    def get_sold(self,product):
        return sum(s.quantity for s in sales.objects.filter(user=self, product=product))
    def get_remaining(self, product):
        return self.get_allocated(product)-self.get_sold(product)
    def unit(self,product) :   
        units=sales.objects.filter(user_id=self,product=product)
        for un in units:
            unit=un.unit
            unit_size=un.unit_size

        
        return unit_size,unit
    
class user_stock_record(models.Model):
    user = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    unit_size = models.FloatField()
    unit = models.CharField(max_length=255)
    allocated = models.FloatField()
    sold = models.FloatField()
    remaining = models.FloatField()
    date = models.DateField()  # Track when the record was made


class our_product(models.Model):
    product_id=models.CharField(max_length=200, primary_key=True)
    product_name=models.CharField(max_length=1000)
    units = models.CharField(max_length=300)
    # cost = models.DecimalField(decimal_places=2, max_digits=60)
    # description = models.TextField()

    def current_stock(self):
        packed=sum(mp.quantity for mp in packing.objects.filter(product=self))
        sold= sum(sale.quantity for sale in sales.objects.filter(product=self))
        allocated = sum(alloc.quantity for alloc in allocation.objects.filter(pack_id=packing.objects.filter(product=self).first()))
        return packed-allocated


    # def unit(self) :   
    #     units=packing.objects.filter(product__product=self)
    #     for un in units:
    #         unit=un.unit
    #         unit_size=un.unit_size

        
    #         return unit_size,unit
    
    def unpacked_stock(self):
        produced=manufactured_products.objects.filter(product=self).aggregate(total=Sum('quantity'))['total'] or 0
        packed =packing.objects.filter(product__product=self)
        packed_litres=0
        for item in packed:
            unit_size=float(item.unit_size)
            qty=item.quantity
            if item.unit.lower()=='ml':
                packed_litres += (unit_size*qty)/1000
            else:
                packed_litres += unit_size*qty    
        return produced-packed_litres
    
class product_variant(models.Model):
    product_var_id=models.CharField(max_length=200, primary_key=True)
    product=models.ForeignKey(our_product, on_delete=models.CASCADE)
    unit_size = models.FloatField()
    unit = models.CharField(max_length=10 )  


    def __str__(self):
        return f"{self.product.product_name}- {self.unit_size}{self.unit}"
    
    def current_stock(self):
        packed=sum(mp.quantity for mp in packing.objects.filter(product=self))
        sold= sum(sale.quantity for sale in sales.objects.filter(product=self))
        allocated = sum(alloc.quantity for alloc in allocation.objects.filter(pack_id=packing.objects.filter(product=self).first()))
        return packed-allocated
    
    

class manufactured_products(models.Model):
    m_id =models.CharField(max_length=200, primary_key=True)
    date = models.DateField(auto_now_add=True)
    product= models.ForeignKey(our_product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    description = models.TextField()
    total  =models.IntegerField()

    def str(self):
        return f"{self.product.product_name}({self.product.units})-{self.quantity}"

class stock(models.Model):
    class Allocation_Status(models.TextChoices):
        ALLOCATED = "ALLOCATED"
        NOT_ALLOCATED = "NOT_ALLOCATED"
          
    stock_id=models.CharField(max_length=200, primary_key=True)
    product_id = models.ForeignKey(manufactured_products, on_delete=models.CASCADE)
    col_allo_stat = models.CharField(max_length = 30,
										choices=Allocation_Status.choices,
										default=Allocation_Status.NOT_ALLOCATED.value)
    quantity = models.IntegerField()


class packing(models.Model):
    pack_id=models.CharField(max_length=255,primary_key=True)
    product=models.ForeignKey(product_variant, on_delete=models.CASCADE)
    quantity=models.FloatField()
    unit_size=models.FloatField()
    unit=models.CharField(max_length=20)
    date=models.DateField()
    
    def str(self):
        f"{self.product.product_name}-Packed{self.quantity}{self.unit}"

    # def unit(self) : 

    #     unit=pu.unit for pu in packing.objects.filter()    
    #     return unit_size,unit    


class allocation(models.Model):
    date = models.DateField(auto_now_add=True)
    user_id = models.ForeignKey(users, on_delete=models.CASCADE)
    pack_id = models.ForeignKey(packing, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_size=models.FloatField()
    units =models.CharField(max_length=300) 
    cost = models.DecimalField(decimal_places=2, max_digits=60)
    total_cost = models.DecimalField(decimal_places=2, max_digits=60)


    def str(self):
        return f" Allocation of {self.pack_id.product.product_name}({self.pack_id.product.units})-{self.quantity} to {self.user_id.full_name}"
   

class sales(models.Model):
    date = models.DateField(default=timezone.now)
    #product_name = models.ForeignKey(stock, on_delete=models.CASCADE)
    product= models.ForeignKey(product_variant, on_delete=models.CASCADE)
    user= models.ForeignKey(users, on_delete=models.CASCADE)
    description = models.TextField()
    quantity = models.IntegerField()
    cost = models.DecimalField(decimal_places=2, max_digits=60)
    status=models.CharField(max_length=20)
    total_cost = models.DecimalField(decimal_places=2, max_digits=60)

    def str(self):
        return f"{self.product.product_name}({self.product.units})-{self.quantity} sold"

class credit_payment(models.Model):
    date=models.DateField()
    user=models.ForeignKey(users, on_delete=models.CASCADE)
    amount=models.DecimalField(decimal_places=2, max_digits=60)


class inventory(models.Model):
    id = models.IntegerField(primary_key=True)
    product_id=models.CharField(max_length=250)
    product_name=models.CharField(max_length=250)
    units = models.CharField(max_length=250)
    total_quantity=models.IntegerField()
    class Meta:
        managed=False
        db_table="product_stock2"



class budget(models.Model):
    budget_id =models.CharField(max_length=255)
    month = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=60,decimal_places=2)

    def str(self):
        return f"{self.month}-{self.amount}"
    
    def total_expenses(self):
        return sum(exp.amount for exp in self.expense_set.all())
    
    def remaining(self):
        return self.amount - self.total_expenses()
    
    def usage_percentage(self):
        if self.amount ==0:
            return 0
        return round((self.total_expenses()/self.amount)*100, 2)
    
class expense_category(models.Model):
    name= models.CharField(max_length=255)


class expense(models.Model):
    expense_id=models.CharField(max_length=255)
    date=models.DateField(default=timezone.now)
    category = models.ForeignKey(expense_category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=60,decimal_places=2)
    budget = models.ForeignKey(budget, on_delete=models.CASCADE)

    def str(self):
        return f"{self.category.name}-{self.amount}"
    
class cashier_report(models.Model):
    class TransactionType(models.TextChoices):
        RECEIVE='RECEIVE','Received from Seller'
        RELEASE='RELEASE', 'Released'

    date =models.DateField()
    source=models.ForeignKey(users, on_delete=models.CASCADE)
    description=models.TextField()
    type=models.CharField(max_length=255,choices=TransactionType.choices, default=TransactionType.RECEIVE)
    amount =models.DecimalField(decimal_places=2, max_digits=65)



   
    

