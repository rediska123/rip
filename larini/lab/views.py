from django.shortcuts import render
from .models import *
import datetime

cart_id = [{
    "customer_name": "Москва ул. Иваново стр. 23/3",
    "order_date": "8 880 554 54 54",
    "items": [{
        "item_id": 1,
        "amount": 12
    }, {
        "item_id": 5,
        "amount": 3
    }, {
        "item_id": 8,
        "amount": 1
    }],
},]
data = [
        {'name': 'Автобусы 30 дней', 'description': 'Удобное и доступное передвижение по городу без ограничений.', 'price': 300, 'id': 0, 'image': 'http://localhost:9000/lab1/bus.png'},
        {'name': 'Автобусы 60 дней', 'description': 'Удобное и доступное передвижение по городу без ограничений.', 'price': 500, 'id': 1, 'image': 'http://localhost:9000/lab1/bus.png'},
        {'name': 'Автобусы 90 дней', 'description': 'Удобное и доступное передвижение по городу без ограничений.', 'price': 700, 'id': 2, 'image': 'http://localhost:9000/lab1/bus.png'},
        {'name': 'Метро 30 дней', 'description': 'Самый быстрый и эффективный способ передвижения по городу.', 'price': 400, 'id': 3, 'image': 'http://localhost:9000/lab1/metro.png'},
        {'name': 'Метро 60 дней', 'description': 'Самый быстрый и эффективный способ передвижения по городу.', 'price': 600, 'id': 4, 'image': 'http://localhost:9000/lab1/metro.png'},
        {'name': 'Метро 90 дней', 'description': 'Самый быстрый и эффективный способ передвижения по городу.', 'price': 800, 'id': 5, 'image': 'http://localhost:9000/lab1/metro.png'},
        {'name': 'МЦД 30 дней', 'description': 'Уникальный гибрид пригородного и городского транспорта.', 'price': 500, 'id': 6, 'image': 'http://localhost:9000/lab1/mcd1.png'},
        {'name': 'МЦД 60 дней', 'description': 'Уникальный гибрид пригородного и городского транспорта.', 'price': 800, 'id': 7, 'image': 'http://localhost:9000/lab1/mcd1.png'},
        {'name': 'МЦД 90 дней', 'description': 'Уникальный гибрид пригородного и городского транспорта.', 'price': 1000, 'id': 8, 'image': 'http://localhost:9000/lab1/mcd1.png'},
        {'name': 'Пригородные электрички 30 дней', 'description': 'Быстрый и вместительный транспорт для поездок за город или по области.', 'price': 600, 'id': 9, 'image': 'http://localhost:9000/lab1/elka.png'},
        {'name': 'Пригородные электрички 60 дней', 'description': 'Быстрый и вместительный транспорт для поездок за город или по области.', 'price': 1000, 'id': 10, 'image': 'http://localhost:9000/lab1/elka.png'},
        {'name': 'Пригородные электрички 90 дней', 'description': 'Быстрый и вместительный транспорт для поездок за город или по области.', 'price': 1400, 'id': 11, 'image': 'http://localhost:9000/lab1/elka.png'},
    ]

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
    if PassOrderItems.objects.filter(pass_order=PassOrder.objects.filter(status=1)[0]).count() != 0:
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
    selected_order = PassOrder.objects.filter(status=1)[0]
    selected_order.status = 2
    selected_order.save()
    printed_count = 0
    selected_cart_id = 0
    selected_cart = PassOrder.objects.filter(status=1)
    if selected_cart.count() != 0:
        selected_cart_id = selected_cart[0].id
        printed_count = PassOrderItems.objects.filter(order=selected_cart_id).count()
    return render(request, 'passes.html', {
        'data': PassItem.objects.all(),
        'cart_count': printed_count,
        'cart_id' : selected_cart_id
    })
