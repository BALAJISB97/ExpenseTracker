from django.shortcuts import render,HttpResponse,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from webapp.models import Income,Expense,Totaldata
from webapp.serializer import IncomeSerializer,ExpenseSerializer,TotaldataSerializer
from django.contrib.auth.models import User,auth,AnonymousUser

class IncomeList(APIView):
    def get(self,request):
        obj = Income.objects.filter(user=request.user).order_by('-IncomeAddedTime')
        serializedObj = IncomeSerializer(obj,many=True)
        return Response(serializedObj.data) 
        
    def post(self,request):
        value = request.data
        sobj = IncomeSerializer(data=request.data,many=False)
        print(sobj)
        if sobj.is_valid():
            print('Not here!! (:')
            sobj.save()
            updateTotalData(request,'income',value)
            return Response(sobj.data,status=status.HTTP_201_CREATED)
        return Response(sobj.errors,status=status.HTTP_400_BAD_REQUEST)


class ExpenseList(APIView):
    def get(self,request):
        obj = Expense.objects.filter(user=request.user).order_by('-ExpenseAddedTime')
        serializedObj = ExpenseSerializer(obj,many=True)
        return Response(serializedObj.data) 
        
    def post(self,request):
        value = request.data
        print('in post request=>data',request.data,)
        
        userObj = Totaldata.objects.get(user=request.user)
        if userObj.TotalIncome > 0:
            perc = round(((request.data['ExpenseValue']/userObj.TotalIncome)*100),2)
            request.data['ExpensePercentage']=perc

        sobj = ExpenseSerializer(data=request.data,many=False)
        print(sobj)
        if sobj.is_valid():
            print('Not here!! (:')
            sobj.save()
            print(sobj)
            updateTotalData(request,'exp',value)
            return Response(sobj.data,status=status.HTTP_201_CREATED)
        return Response(sobj.errors,status=status.HTTP_400_BAD_REQUEST)



def updateTotalData(request,typee,value):
    #1.check if the user has total obj 
    #2. If not create one and add
    #else get the obj and update type value and total budget and percentage!
    if Totaldata.objects.filter(user=request.user).exists():
        obj = Totaldata.objects.get(user=request.user)
        print('not here')
        updateValueBasedOnType(request,typee,obj,value)
    else:
        print('unexpected!')
        obj = Totaldata(user=request.user)
        updateValueBasedOnType(request,typee,obj,value)

def updateValueBasedOnType(request,typee,obj,value):
    flag = False
    if typee=='income':
        obj.TotalIncome+=value['IncomeValue']
        flag = True
    else:
        obj.TotalExpense+=value['ExpenseValue']
    
    obj.TotalBudget = obj.TotalIncome - obj.TotalExpense
    #calculate percentage for income
    if obj.TotalIncome > 0:
        obj.Percentage = round(((obj.TotalExpense/obj.TotalIncome)*100),2)
    obj.save()
    if flag:calculatePercentage(request)

def calculatePercentage(request):
    expenseObjs = Expense.objects.filter(user=request.user)
    Totalobj = Totaldata.objects.get(user=request.user)
    TotalIncomeValue = Totalobj.TotalIncome
    for obj in expenseObjs:
        obj.ExpensePercentage = round(((obj.ExpenseValue/TotalIncomeValue)*100),2)
        obj.save()

def Delete(request,typee,val):
    obj = Totaldata.objects.get(user=request.user)
    if typee=='exp':
        obj.TotalExpense-=val
    else:
        obj.TotalIncome-=val
    if obj.TotalIncome > 0:
        obj.TotalBudget=(obj.TotalIncome-obj.TotalExpense)
    else:
        obj.TotalBudget=0
    if obj.TotalIncome > 0:
        obj.Percentage = round(((obj.TotalExpense/obj.TotalIncome)*100),2)
    else:
        obj.Percentage=0
    obj.save()
    calculatePercentage(request)

        
class TotaldataList(APIView):
    def get(self,request):
        obj = Totaldata.objects.filter(user=request.user)
        serializedObj = TotaldataSerializer(obj,many=True)
        return Response(serializedObj.data)


# Create your views here.
class DeleteIncome(APIView):

    def getObject(self,pk):
        try:
            obj = Income.objects.get(pk=pk)
            return obj
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,pk):
        sobj = self.getObject(pk)
        nsobj = IncomeSerializer(sobj)
        print(nsobj.data,nsobj)
        return Response(nsobj.data)
    
    def put(self,request,pk):
        sobj = self.getObject(pk)
        sobj = IncomeSerializer(sobj,data=request.data)
        if sobj.is_valid():
            sobj.save()
            return Response(sobj.data,status=status.HTTP_201_CREATED)
        return Response(sobj.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        print('delete called!')
        obj = self.getObject(pk)
        val = obj.IncomeValue
        obj.delete()
        Delete(request,'inc',val)
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteExpense(APIView):

    def getObject(self,pk):
        try:
            obj = Expense.objects.get(pk=pk)
            return obj
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,pk):
        sobj = self.getObject(pk)
        nsobj = ExpenseSerializer(sobj)
        print(nsobj.data,nsobj)
        return Response(nsobj.data)
    
    def put(self,request,pk):
        sobj = self.getObject(pk)
        sobj = ExpenseSerializer(sobj,data=request.data)
        if sobj.is_valid():
            sobj.save()
            return Response(sobj.data,status=status.HTTP_201_CREATED)
        return Response(sobj.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        print('delete called!')
        obj = self.getObject(pk)
        val = obj.ExpenseValue
        obj.delete()
        Delete(request,'exp',val)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class checkLoginStatus(APIView):
    def get(self,request):
        user = {'isLoggedIn':False}
        if request.user!=AnonymousUser():
            user['isLoggedIn']=True
            user['userid']=request.user.id
            print(request.user.id)
        return Response(data=user)
