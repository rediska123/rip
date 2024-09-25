from django.shortcuts import render


cart_id = [{
    "customer_address": "Москва ул. Иваново стр. 23/3",
    "customer_phone": "8 880 554 54 54",
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
    print(pass_price)
    if(pass_price != None):
        pass_price = int(pass_price)
        result = []
        for i in data:
            if i['price'] < pass_price:
                result.append(i)
        print(result)
        return render(request, 'passes.html', {
        'data': result,
        'searched_price': pass_price,
        'cart': len(cart_id[0]["items"])
        })
    return render(request, 'passes.html', {
        'data': data,
        'cart': len(cart_id[0]["items"])
    })


def GetPass(request, id):
    return render(request, 'pass.html', {
        'data': data[id],
        'cart': len(cart_id[0]["items"])
    })
# Create your views here.

def GetCart(request, id):
    result = cart_id[id]
    result["final_price"] = 0
    for i in data:
        for j in result["items"]:
            if i['id'] == j['item_id']:
                j["name"] = i["name"]
                j["description"] = i["description"]
                j["price"] = i["price"]
                j["image"] = i["image"]
                result["final_price"] += j["price"] * j["amount"]
    return render(request, 'cart.html', result)

def searchPasses(request, pass_price):
    print("hellow")
    result = []
    for i in data:
        if i['price'] < pass_price:
            result.append(i)
    print(result)
    return render(request, 'passes.html', {
        'data': result,
    })