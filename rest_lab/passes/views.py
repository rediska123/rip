from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from passes.serializer import *
from passes.models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser, FormParser
from passes.stocks.minio import add_pic, del_pic
import datetime

# Create your views here.

def user():
    try:
        user1 = AuthUser.objects.get(id=2)
    except:
        user1 = AuthUser(id=2, first_name="Иван", last_name="Иванов", password=1234, username="user1")
        user1.save()
    return user1

@api_view(["GET", "POST"])
def pass_catalog(request):
    if request.method == 'GET':
        try:
            parsed_data = JSONParser().parse(request)
            if parsed_data['price'] != None:
                passes = PassItem.objects.filter(price__lte = parsed_data['price'])
            else:
                passes = PassItem.objects.all()
        except:
            passes = PassItem.objects.all()
        serializer = PassSerializer(passes, many=True)
        printed_count = None
        selected_client_card_id = None
        selected_user = user()
        selected_client_card = PassOrder.objects.filter(status=1, user=selected_user.id)
        if selected_client_card.count() != 0:
            selected_client_card_id = selected_client_card[0].id
            printed_count = PassOrderItems.objects.filter(pass_client_card=selected_client_card_id).count()
        response = {
            "passes": serializer.data,
            "cart_id": selected_client_card_id,
            "cart_count": printed_count,
            "user_id": selected_user.id
        }
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        parsed_data = JSONParser().parse(request)
        serializer = PassSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE", "POST"])
def pass_item(request, id):
    try: 
        selected_pass = PassItem.objects.get(id=id) 
    except PassItem.DoesNotExist: 
        return Response({"message": "Pass not found!"}, status=status.HTTP_200_OK)
    if request.method == 'GET':
        serializer = PassSerializer(selected_pass)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        parsed_data = JSONParser().parse(request)
        if 'pic' in parsed_data:
            pic_result = add_pic(selected_pass, parsed_data.initial_data['pic'])
            if 'error' in pic_result.data:
                return Response({"message": pic_result}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PassSerializer(selected_pass, data=parsed_data, partial=True) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE':
        pic_result = del_pic(selected_pass)
        if 'error' in pic_result:
            return Response({"message": pic_result}, status=status.HTTP_400_BAD_REQUEST)
        selected_pass.delete() 
        return Response({"message": "Pass was deleted successfully!"}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # Используем MultiPartParser для обработки файлов
        pic_file = request.FILES['pic']
        # Проверяем наличие файла в parsed_data
        if pic_file != None:
            pic_result = add_pic(selected_pass, pic_file)
            if 'error' in pic_result:
                return Response({"message": pic_result}, status=status.HTTP_400_BAD_REQUEST)
            selected_pass.image = pic_result["message"]
            selected_pass.save()
            serializer = PassSerializer(PassItem.objects.get(id=id) ) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Not a image!"}, status=status.HTTP_400_BAD_REQUEST) 
    

@api_view(["GET", "POST"])
def pass_client_cards(request):
    if request.method == 'GET':
        try:
            parsed_data = JSONParser().parse(request)
            if 'status' in parsed_data.keys() and 'start_date' in parsed_data.keys() and 'end_date' in parsed_data.keys():
                orders = PassItem.objects.filter(status=parsed_data['status'],
                                                 created_date__range=(parsed_data['start_date'], parsed_data['end_date']))
            elif 'status' in parsed_data.keys():
                orders = PassOrder.objects.filter(status=parsed_data['status'])
            elif 'start_date' in parsed_data.keys() and 'end_date' in parsed_data.keys():
                orders = PassOrder.objects.filter(created_date__range=(parsed_data['start_date'], parsed_data['end_date']),
                                                  status__gte = 3)
            else:
                orders =  PassOrder.objects.filter(status__gte = 3).order_by('created_date', 'status')
        except:
            orders =  PassOrder.objects.filter(status__gte = 3).order_by('created_date', 'status')
        if orders.count() == 0:
            orders = None
        serializer = ClientCardSerializer(orders, many=True)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        parsed_data = JSONParser().parse(request)
        serializer = ClientCardSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def pass_client_card(request, id):
    try: 
        selected_client_card = PassOrder.objects.get(id=id) 
    except PassOrder.DoesNotExist: 
        return Response(None, status=status.HTTP_200_OK)
    if request.method == 'GET':
        serializer = ClientCardDetailsSerializer(selected_client_card)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        parsed_data = JSONParser().parse(request)
        serializer = EditClientCardSerializer(selected_client_card, data=parsed_data, partial=True) 
        if serializer.is_valid(): 
            serializer.save()
            serializer = ClientCardDetailsSerializer(PassOrder.objects.get(id=id))
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE':
        selected_client_card.status = 2
        selected_client_card.save() 
        return Response({"message": "Order was deleted successfully!"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def add_pass_to_client_card(request, id):
    parsed_data = JSONParser().parse(request)
    if parsed_data['amount'] == None:
        return Response({"message": "No amount!"}, status=status.HTTP_400_BAD_REQUEST)
    selected_user = user()
    try:
        selected_pass = PassItem.objects.get(id=id)
    except PassItem.DoesNotExist:
        return Response({"message": "Product with id={id} not found"}, status=status.HTTP_400_BAD_REQUEST)
    try: 
        selected_client_card = PassOrder.objects.get(user=selected_user, status=1) 
    except PassOrder.DoesNotExist: 
        selected_client_card = PassOrder(user=selected_user, status=1)
        selected_client_card.save()
    try: 
        selected_client_card_item = PassOrderItems.objects.get(pass_client_card=selected_client_card, pass_item=selected_pass) 
    except PassOrderItems.DoesNotExist: 
        selected_client_card_item = PassOrderItems(pass_client_card=selected_client_card, pass_item=selected_pass, amount=0)
    selected_client_card_item.amount += parsed_data['amount']
    selected_client_card_item.save()
    selected_client_card_items = PassOrderItems.objects.filter(pass_client_card=selected_client_card)
    serializer = ClientCardPassSerializer(selected_client_card_items, many=True)
    response = serializer.data
    return Response(response, status=status.HTTP_200_OK)


@api_view(["POST", "PUT"])
def user_registration(request):
    parsed_data = JSONParser().parse(request)
    if request.method == 'POST':
        serializer = UserSerializer(data=parsed_data)
        if serializer.is_valid():
            try:
                serializer.save()
            except:
                return Response({"message": "Used username"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        try:
            user = AuthUser.objects.get(username = parsed_data['username'], password = parsed_data['password'])
        except AuthUser.DoesNotExist:
            return Response({"message": "Cant login"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EditUserSerializer(user, data=parsed_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"message": "Bad data"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def user_auth(request):
    parsed_data = JSONParser().parse(request)
    try:
        user = AuthUser.objects.get(username = parsed_data['username'], password = parsed_data['password'])
    except AuthUser.DoesNotExist:
        return Response({"message": "Cant login"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "login succesfuly"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def user_deauth(request):
    parsed_data = JSONParser().parse(request)
    try:
        user = AuthUser.objects.get(username = parsed_data['username'], password = parsed_data['password'])
    except AuthUser.DoesNotExist:
        return Response({"message": "Cant logout"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "logout succesfuly"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def submit_client_card(request, id):
    try: 
        selected_client_card = PassOrder.objects.get(id=id, status=1) 
    except PassOrder.DoesNotExist: 
        return Response({"message": "Order not found"}, status=status.HTTP_400_BAD_REQUEST)
    if selected_client_card.name != None and selected_client_card.phone != None:
        selected_client_card.status = 3
        selected_client_card.submited_date = datetime.datetime.now()
        selected_client_card.save()
        serializers = ClientCardDetailsSerializer(selected_client_card)
        return Response(serializers.data, status=status.HTTP_200_OK)
    return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def accept_client_card(request, id):
    try: 
        selected_client_card = PassOrder.objects.get(id=id, status=3) 
    except PassOrder.DoesNotExist: 
        return Response({"message": "Order not found"}, status=status.HTTP_400_BAD_REQUEST)
    if selected_client_card.name != None and selected_client_card.phone != None and selected_client_card.submited_date != None:
        selected_client_card.status = 4
        selected_client_card.moderator = AuthUser.objects.get(username="admin")
        selected_client_card.accepted_date = datetime.datetime.now()
        selected_client_card.save()
        serializers = ClientCardSerializer(selected_client_card)
        return Response(serializers.data, status=status.HTTP_200_OK)
    return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "DELETE"])
def pass_client_card_pass(request, id):
    try: 
        selected_client_card_pass = PassOrderItems.objects.get(id=id) 
    except PassOrderItems.DoesNotExist: 
        return Response({"message": "Pass not found"}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        parsed_data = JSONParser().parse(request)
        serializer = ClientCardPassSerializer(selected_client_card_pass, data=parsed_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        selected_client_card_pass.delete()
        return Response({"message": "Deleted succesfuly"}, status=status.HTTP_200_OK)