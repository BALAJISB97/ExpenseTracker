from rest_framework import serializers
from webapp.models import Income,Expense,Totaldata

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"

class TotaldataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Totaldata
        fields = "__all__"
        