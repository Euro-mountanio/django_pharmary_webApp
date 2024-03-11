from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('medication/', views.medication, name='medication'),
    path('search/',views.search, name='search'),
    path('customer_medication/', views.customer_medication, name='customer_medication'),
    path('drug/', views.sold_drug, name='drug'),
    path('update_drug/<int:pk>', views.update_drug, name='update_drug'),
    path('delete_drug/<int:pk>', views.delete_drug, name='delete_drug'),
    path('view_drugs/', views.view_drugs, name='view_drugs'),
    path('drug_record/<int:pk>', views.view_drug_record, name='drug_record'),


]