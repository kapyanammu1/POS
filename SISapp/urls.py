from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('items/', views.item_list, name='item_list'),
    path('Signup/', views.Signup, name='Signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('logout/', views.logout_view, name='logouts'),
    path('Items/', views.tables_data, name='tables_data'),
    path('AddItems/', views.AddItem, name='AddItems'),
    path('EditItems/<int:pk>/edit/', views.EditItems, name='EditItems'),
    path('deleteItems/<int:pk>/delete/', views.deleteItems, name='deleteItems'),
    path('CategoryForm/', views.CategoryForm, name='CategoryForm'),
    path('AddCategory/', views.AddCategory, name='AddCategory'),
    path('EditCategory/<int:pk>/edit/', views.EditCategory, name='EditCategory'),
    path('deleteCategory/<int:pk>/delete/', views.deleteCategory, name='deleteCategory'),
    path('deleteOrder/<int:pk>/delete/', views.deleteOrder, name='deleteOrder'),
    path('CustomerForm/', views.CustomerForm, name='CustomerForm'),
    path('AddCustomer/', views.AddCustomer, name='AddCustomer'),    
    path('EditCustomer/<int:pk>/edit/', views.EditCustomer, name='EditCustomer'),
    path('deleteCustomer/<int:pk>/delete/', views.deleteCustomer, name='deleteCustomer'),
    path('Order_ListForm/', views.Order_ListForm, name='Order_ListForm'),
    path('OrderForm/', views.OrderForm, name='OrderForm'),
    path('Payment/<int:pk>/', views.Payment, name='Payment'),
    path('Order_Items/<int:pk>/', views.Order_Items, name='Order_Items'),
    path('Edit_Order/<int:pk>/', views.Edit_Order, name='Edit_Order'),
    path('DeleteOrder_Items/<int:pk>/delete/', views.DeleteOrder_Items, name='DeleteOrder_Items'),
    path('deleteSales/<int:pk>/delete/', views.deleteSales, name='deleteSales'),
    path('Sales/', views.SalesForm, name='Sales'),
    path('get_order_items/', views.get_order_items, name='get_order_items'),
]