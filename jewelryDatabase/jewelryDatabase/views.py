from pyexpat.errors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.template import loader
from jewelryDatabase.forms import addSupplierForm
from .models import Item
from django.db import connection
from django.contrib.auth.forms import UserCreationForm

def index(request):
    print(request.user)
    return render(request, 'index.html')

def customerlist(request):
    template = loader.get_template('customerlist.html')
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT ID, FirstName, LastName, Email FROM Person WHERE Customer = 1")
        row = cursor.fetchall()
        context = {
            'row': row,
        }
    print(row)
    return HttpResponse(template.render(context, request))

def findemployee(request):
    template = loader.get_template('findemployee.html')
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT Employee.StoreID, Employee.PersonID, Employee.ESSN, Person.FirstName, Person.LastName, Person.Email FROM Employee, Person WHERE Employee.PersonID = ID")
        row = cursor.fetchall()
        context = {
            'row': row,
        }
    print(row)
    return HttpResponse(template.render(context, request))

def purchaseHistory(request):
    template = loader.get_template('purchase.html')
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM Purchase JOIN Person ON Person.ID = Purchase.PersonID")
        row = cursor.fetchall()
        context = {
            'row': row,
        }
    print(row)
    return HttpResponse(template.render(context, request))

def items(request):
    template = loader.get_template('items.html')
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM Item")
        row = cursor.fetchall()
        context = {
            'row': row,
        }
    return HttpResponse(template.render(context, request))

def filterItem(request):
    searchWord = request.POST.get('system', None)
    template = loader.get_template('items/lookup.html')
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM Item WHERE Type = %s", [searchWord])
        row = cursor.fetchall()
        context = {
            'row': row,
        }
    print(row)
    return HttpResponse(template.render(context, request))

def supplier(request):
    template = loader.get_template('supplier.html')
    print(template)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Supplier")
        row = cursor.fetchall()
        context = {
            'row': row,
        }
    print(row)
    return HttpResponse(template.render(context, request))

def deleteSupplier(request):
    if request.method == 'POST':
        supplierID = request.POST.get('deletesupplier', None)
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Supplier WHERE SupplierID = %s", [supplierID])
            return redirect('/supplier')
    return render(request,'suppliers/deletesupplier.html')

def deleteItem(request):
    if request.method == 'POST':
        itemid = request.POST.get('deleteitem', None)
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Item WHERE Item.ItemID = %s", [itemid])
            return redirect('/items')
    return render(request, 'items/deleteitem.html')

def store(request):
    template = loader.get_template('store.html')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Store")
        row = cursor.fetchall()
        context = {
            'row': row,
        }
    print(row)
    return HttpResponse(template.render(context, request))

def rawInventory(request):
    template = loader.get_template('rawInventory.html')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Gems")
        row = cursor.fetchall()
        context = {
            'row': row,
        }
    print(row)
    return HttpResponse(template.render(context, request))

# def register(request):
#     if request.POST == 'POST':
#         form = UserCreationForm()
#         if form.is_valid():
#             form.save()
#         messages.success(request, 'Account created successfully')
#     else:
#         form = UserCreationForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'register.html', context)

def addEmployee(request):
    form = addEmployeeForm()
    context = {
        'form':form,
    }
    return render(request, 'addemployee.html', context)

def addItem(request):
    if request.method == 'POST': 
        barcode = request.POST.get('barcode', None)
        weight = request.POST.get('weight', None)
        price = request.POST.get('price', None)
        type = request.POST.get('type', None)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Item (Barcode, Weight, Price, Type) VALUES (%s, %s, %s, %s)", (barcode, weight, price, type))
            # cursor.execute("INSERT INTO SoldAt(StoreID, ItemID, ItemBarcode, Stock) VALUES (%s, %s, %s, %s)", storeid, itemid, barcode, stock)
            return redirect('/items')
    return render(request, 'items/additem.html')
    
def deleteItem(request):
    if request.method == 'POST':
        itemid = request.POST.get('deleteitem', None)
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Item WHERE Item.ItemID = %s", [itemid])
            return redirect('/items')
    return render(request, 'items/deleteitem.html')

def addSupplier(request):
    form = addSupplierForm()
    if request.method == 'POST':
        form = addSupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier')
    context = {
        'form': form,
    }
    return render(request, 'suppliers/addsupplier.html', context)


