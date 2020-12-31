from django.db import models
from django.conf import settings

# Create your models here.
class Income(models.Model):
    IncomeValue=models.FloatField()
    Description = models.TextField()
    IncomeAddedTime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)


class Expense(models.Model):
    ExpenseValue = models.FloatField()
    Description = models.TextField()
    ExpenseAddedTime = models.DateTimeField(auto_now_add=True)
    ExpensePercentage = models.FloatField(default=-1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)


class Totaldata(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    TotalIncome = models.FloatField(default=0)
    TotalExpense = models.FloatField(default=0)
    TotalBudget = models.FloatField(default=0)
    Percentage = models.FloatField(default=-1)