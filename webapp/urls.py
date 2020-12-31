from django.contrib import admin
from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from webapp import views


urlpatterns = [
    path('income',views.IncomeList.as_view()),
    path('expense',views.ExpenseList.as_view()),
    path('totaldata',views.TotaldataList.as_view()),
    path('user',views.checkLoginStatus.as_view()), 
    path('deleteIncome/<int:pk>',views.DeleteIncome.as_view()),
    path('deleteExpense/<int:pk>',views.DeleteExpense.as_view()),   
    
]