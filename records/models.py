from django.db import models
from django.utils import timezone

# Create your models here.
class users(models.Model):
    user_id = models.CharField(max_length=200, primary_key=True)
    full_name= models.CharField(max_length=200)
    def str(self):
        return f"{self.full_name} ({self.user_id})"

    def get_allocated(self,product):
        return sum(a.quantity for a in allocation.objects.filter(user_id=self, man_id= manufactured_products.objects.filter(product=product).first()))
    
    def get_sold(self,product):
        return sum(s.quantity for s in sales.objects.filter(user=self, product=product))
    def get_remaining(self, product):
        return self.get_allocated(product)-self.get_sold(product)
    
    

class our_product(models.Model):
    product_id=models.CharField(max_length=200, primary_key=True)
    product_name=models.CharField(max_length=1000)
    units = models.CharField(max_length=300)
    cost = models.DecimalField(decimal_places=2, max_digits=60)
    description = models.TextField()

    def current_stock(self):
        produced=sum(mp.quantity for mp in manufactured_products.objects.filter(product=self))
        sold= sum(sale.quantity for sale in sales.objects.filter(product=self))
        allocated = sum(alloc.quantity for alloc in allocation.objects.filter(man_id=manufactured_products.objects.filter(product=self).first()))
        return produced-allocated

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

class allocation(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(users, on_delete=models.CASCADE)
    man_id = models.ForeignKey(manufactured_products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    units =models.CharField(max_length=300) 

    def str(self):
        return f" Allocation of {self.man_id.product.product_name}({self.man_id.product.units})-{self.quantity} to {self.user_id.full_name}"
   

class sales(models.Model):
    date = models.DateField(default=timezone.now)
    #product_name = models.ForeignKey(stock, on_delete=models.CASCADE)
    product= models.ForeignKey(our_product, on_delete=models.CASCADE)
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


   
    

