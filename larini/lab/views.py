from django.shortcuts import render, redirect
from .models import *
import datetime

from django.db import connection


def GetPasses(request):
    pass_price = request.GET.get("pass-price")
    printed_count = 0
    selected_cart_id = 0
    selected_cart = PassOrder.objects.filter(status=1)
    if selected_cart.count() != 0:
        selected_cart_id = selected_cart[0].id
        printed_count = PassOrderItems.objects.filter(pass_order=selected_cart_id).count()
    if pass_price != None:
        return render(request, 'passes.html', {
            'data': PassItem.objects.filter(price__lte = int(pass_price)),
            'searched_price': pass_price,
            'cart_count': printed_count,
            'cart_id' : selected_cart_id
        })
    return render(request, 'passes.html', {
        'data': PassItem.objects.all(),
        'cart_count': printed_count,
        'cart_id' : selected_cart_id
    })

def GetPass(request, selected_id):
    printed_count = 0
    selected_cart_id = 0
    selected_cart = PassOrder.objects.filter(status=1)
    if selected_cart.count() != 0:
        selected_cart_id = selected_cart[0].id
        printed_count = PassOrderItems.objects.filter(pass_order=selected_cart_id).count()
    return render(request, 'pass.html', {
        'data': PassItem.objects.filter(id=selected_id).first(),
        'cart_count': printed_count,
        'cart_id' : selected_cart_id
        })
    
def GetCart(request, id):
    try:
        ord = PassOrder.objects.get(id=id)
        if ord.status == 2:
            raise ord.DoesNotExist 
    except ord.DoesNotExist:
        return render(request, 'cart.html', {"error": True, "error_message": "Заказ удален"})
    a = PassOrderItems.objects.filter(pass_order=PassOrder.objects.filter(status=1)[0]).select_related('pass_item')
    final_price = 0
    for i in a:
        final_price += i.pass_item.price * i.amount
    test_date = PassOrderItems.objects.select_related('pass_item').filter(pass_order=PassOrder.objects.filter(status=1)[0])
    print(test_date)
    return render(request, 'cart.html', {
        'data': PassOrderItems.objects.filter(pass_order=PassOrder.objects.filter(status=1)[0]).select_related('pass_item'),
        'final_price': final_price,
        'cart_id': id
    })

def AddPassItem(request):
    writing_count = request.POST['this_pass_count']
    writing_pass =request.POST['selected_pass']
    print(writing_pass)
    started_order = PassOrder.objects.filter(status=1).count()
    if started_order == 0:
        new_order = PassOrder(created_date = datetime.date.today(), status = 1)
        new_order.save()
    if PassOrderItems.objects.filter(pass_order=PassOrder.objects.filter(status=1)[0], pass_item=PassItem.objects.filter(id=writing_pass)[0]).count() != 0:
        selected_item = PassOrderItems.objects.filter(pass_order=PassOrder.objects.filter(status=1)[0])[0]
        selected_item.amount += int(writing_count)
        selected_item.save()
    else:
        for_key = PassOrder.objects.filter(status=1)[0]
        ps_id = PassItem.objects.filter(id=writing_pass)[0]
        item = PassOrderItems(pass_order=for_key, pass_item=ps_id, amount=int(writing_count))
        item.save()
    printed_count = 0
    selected_cart_id = 0
    selected_cart = PassOrder.objects.filter(status=1)
    if selected_cart.count() != 0:
        selected_cart_id = selected_cart[0].id
        printed_count = PassOrderItems.objects.filter(pass_order=selected_cart_id).count()
    
    return render(request, 'passes.html', {
        'data': PassItem.objects.all(),
        'cart_count': printed_count,
        'cart_id' : selected_cart_id
    })

def DelPassItem(request, selected_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE lab_passorder SET status = 2 WHERE id = %s", [selected_id])
    printed_count = 0
    selected_cart_id = 0
    selected_cart = PassOrder.objects.filter(status=1)
    if selected_cart.count() != 0:
        selected_cart_id = selected_cart[0].id
        printed_count = PassOrderItems.objects.filter(order=selected_cart_id).count()
    return redirect('/')
    return render(request, 'passes.html', {
        'data': PassItem.objects.all(),
        'cart_count': printed_count,
        'cart_id' : selected_cart_id
    })
