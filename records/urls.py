from django.urls import path
from .import views
from . import models
from django.contrib.auth import views as auth_views
from .views import home

app_name='records'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('home/', home, name='home'),
    path('logout', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('products', views.products, name='products'),
    path('sales', views.sales_report, name='sales'),
    path('manufactured_product', views.manufactured_product, name='manufactured_product'),
    path('staff', views.staff, name='staff'),
    path('stocking', views.stocking, name='stocking'),
    path('allocating', views.allocating, name='allocating'),
    path('currency', views.curr, name='currency'),
    path('product_list', views.product_list, name='product_list'),
    path('user_report', views.user_stock_report, name='user_report'),
    path('budgeting', views.budgeting, name='budget'),
    path('expenses', views.expenses, name='expenses'),
    path('category', views.category, name='category'),
    path('budget_report', views.budget_report, name='budget_report'),
    path('credit_payments', views.credit_payments, name='credits')
   
   
]
