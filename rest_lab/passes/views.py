from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from passes.serializer import *
from passes.models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser, FormParser
from passes.stocks.minio import add_pic, del_pic
import datetime

from drf_yasg.utils import swagger_auto_schema
from passes.permission import *
from passes.redis import session_storage
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import *
from django.views.decorators.csrf import csrf_exempt
import uuid
import hashlib
import base64


# Create your views here.

def get_user(request):
    session_id = request.COOKIES.get("session_id")
    if session_id is None:
        return None
    else:
        username = session_storage.get(session_id).decode("utf-8")
        try:
            user = User.objects.get(username=username)
            print(user.username)
            return user
        except:
            print("cant get user")
            user = None
            return user


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes        
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator


class pass_catalog(APIView):
    def get(self, request):
        try:
            price = request.GET.get("price")
            if price != None:
                passes = PassItem.objects.filter(price__lte = price)
            else:
                passes = PassItem.objects.all()
        except:
            passes = PassItem.objects.all()
        serializer = PassSerializer(passes, many=True)
        printed_count = None
        selected_client_card_id = None
        selected_user = get_user(request)
        if selected_user is not None:
            selected_client_card = PassOrder.objects.filter(status=1, user=selected_user.id)
            if selected_client_card.count() != 0:
                selected_client_card_id = selected_client_card[0].id
                printed_count = PassOrderItems.objects.filter(pass_order=selected_client_card_id).count()
        response = {
            "passes": serializer.data,
            "client_card_id": selected_client_card_id,
            "client_card_count": printed_count,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=PassSerializer)
    @method_permission_classes([IsAdminAuth])
    def post(self, request):
        parsed_data = JSONParser().parse(request)
        serializer = PassSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class pass_item(APIView):
    def get(self, request, id):
        try: 
            selected_pass = PassItem.objects.get(id=id) 
        except PassItem.DoesNotExist: 
            return Response({"message": "Pass not found!"}, status=status.HTTP_200_OK)
        serializer = PassSerializer(selected_pass)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=PassSerializer)
    @method_permission_classes([IsAdminAuth])
    def put(self, request, id):
        try: 
            selected_pass = PassItem.objects.get(id=id) 
        except PassItem.DoesNotExist: 
            return Response({"message": "Pass not found!"}, status=status.HTTP_200_OK)
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
    
    @method_permission_classes([IsAdminAuth])
    def delete(self, request, id):
        try: 
            selected_pass = PassItem.objects.get(id=id) 
        except PassItem.DoesNotExist: 
            return Response({"message": "Pass not found!"}, status=status.HTTP_200_OK)
        pic_result = del_pic(selected_pass)
        if 'error' in pic_result:
            return Response({"message": pic_result}, status=status.HTTP_400_BAD_REQUEST)
        selected_pass.delete() 
        return Response({"message": "Pass was deleted successfully!"}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=PassSerializer)
    @method_permission_classes([IsAdminAuth])
    def post(self, request, id):
        try: 
            selected_pass = PassItem.objects.get(id=id) 
        except PassItem.DoesNotExist: 
            return Response({"message": "Pass not found!"}, status=status.HTTP_200_OK)
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


class pass_client_cards(APIView):
    @method_permission_classes([IsAuth])
    def get(self, request):
        user = get_user(request)
        if user.is_staff or user.is_superuser:
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
                    orders =  PassOrder.objects.filter(status__gte = 3)
            except:
                orders =  PassOrder.objects.filter(status__gte = 3)
        else:
            try:
                parsed_data = JSONParser().parse(request)
                if 'status' in parsed_data.keys() and 'start_date' in parsed_data.keys() and 'end_date' in parsed_data.keys():
                    orders = PassItem.objects.filter(status=parsed_data['status'],
                                                 created_date__range=(parsed_data['start_date'], parsed_data['end_date']),
                                                 user=user)
                elif 'status' in parsed_data.keys():
                    orders = PassOrder.objects.filter(status=parsed_data['status'], user=user)
                elif 'start_date' in parsed_data.keys() and 'end_date' in parsed_data.keys():
                    orders = PassOrder.objects.filter(created_date__range=(parsed_data['start_date'], parsed_data['end_date']),
                                                  user=user)
                else:
                    orders =  PassOrder.objects.filter(user=user)
            except:
                orders =  PassOrder.objects.filter(user=user)
        if orders.count() == 0:
            orders = None
        serializer = ClientCardSerializer(orders, many=True)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)

class pass_client_card(APIView):
    @method_permission_classes([IsAuth])  
    def get(self, request, id):
        user = get_user(request)
        if user.is_staff or user.is_superuser:
            try: 
                selected_client_card = PassOrder.objects.get(id=id) 
            except PassOrder.DoesNotExist: 
                return Response({"message": "Client card does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try: 
                selected_client_card = PassOrder.objects.get(id=id, user=user) 
            except PassOrder.DoesNotExist: 
                return Response({"message": "Client card does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ClientCardDetailsSerializer(selected_client_card)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(request_body=EditClientCardSerializer) 
    @method_permission_classes([IsAuth])    
    def put(self, request, id):
        user = get_user(request)
        if user.is_staff or user.is_superuser:
            try: 
                selected_client_card = PassOrder.objects.get(id=id) 
            except PassOrder.DoesNotExist: 
                return Response({"message": "Client card does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try: 
                selected_client_card = PassOrder.objects.get(id=id, user=user) 
            except PassOrder.DoesNotExist: 
                return Response({"message": "Client card does not exist user"}, status=status.HTTP_400_BAD_REQUEST)
        parsed_data = JSONParser().parse(request)
        serializer = EditClientCardSerializer(selected_client_card, data=parsed_data, partial=True) 
        if serializer.is_valid(): 
            serializer.save()
            serializer = ClientCardDetailsSerializer(PassOrder.objects.get(id=id))
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    @method_permission_classes([IsAuth])    
    def delete(self, request, id):
        user = get_user(request)
        if user.is_staff or user.is_superuser:
            try: 
                selected_client_card = PassOrder.objects.get(id=id) 
            except PassOrder.DoesNotExist: 
                return Response({"message": "Client card does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try: 
                selected_client_card = PassOrder.objects.get(id=id, user=user) 
            except PassOrder.DoesNotExist: 
                return Response({"message": "Client card does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        selected_client_card.status = 2
        selected_client_card.save() 
        return Response({"message": "Client card was deleted successfully!"}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=ClientCardPassSerializer)
@permission_classes([IsAdminAuth])   
@api_view(["POST"])
def add_pass_to_client_card(request, id):
    parsed_data = JSONParser().parse(request)
    if parsed_data['amount'] == None:
        return Response({"message": "No amount!"}, status=status.HTTP_400_BAD_REQUEST)
    selected_user = get_user(request)
    try:
        selected_pass = PassItem.objects.get(id=id)
    except PassItem.DoesNotExist:
        return Response({"message": "Pass with id={id} not found"}, status=status.HTTP_400_BAD_REQUEST)
    try: 
        selected_client_card = PassOrder.objects.get(user=selected_user, status=1) 
    except PassOrder.DoesNotExist: 
        selected_client_card = PassOrder(user=selected_user, status=1)
        selected_client_card.save()
    try: 
        selected_client_card_item = PassOrderItems.objects.get(pass_order=selected_client_card, pass_item=selected_pass) 
    except PassOrderItems.DoesNotExist: 
        selected_client_card_item = PassOrderItems(pass_order=selected_client_card, pass_item=selected_pass, amount=0)
    selected_client_card_item.amount += parsed_data['amount']
    selected_client_card_item.save()
    selected_client_card_items = PassOrderItems.objects.filter(pass_order=selected_client_card)
    serializer = ClientCardPassSerializer(selected_client_card_items, many=True)
    response = serializer.data
    return Response(response, status=status.HTTP_200_OK)

@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(["POST"])
def user_registration(request):
    parsed_data = JSONParser().parse(request)
    serializer = UserSerializer(data=parsed_data)
    if serializer.is_valid():
        try:
            serializer.save()
        except:
            return Response({"message": "Used username"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(method='put', request_body=EditUserSerializer)
@permission_classes([IsAuth])   
@api_view(["PUT"])
def user_edit(request):
    parsed_data = JSONParser().parse(request)
    try:
        user = User.objects.get(username = parsed_data['username'], password = parsed_data['password'])
    except User.DoesNotExist:
        return Response({"message": "Cant login"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = EditUserSerializer(user, data=parsed_data, partial=True)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({"message": "Bad data"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_200_OK)




@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(["POST"])
@permission_classes([AllowAny])
def user_auth(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username,
                            password=password)
    if user is not None:
        login(request, user)
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie("session_id", random_key, samesite="lax")
        return response
    else:
        return Response({"message": "Cant login",
                             "username":username,
                             "password":password},
                            status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(method='post')
@api_view(["POST"])
def user_deauth(request):
    session_id = request.COOKIES.get("session_id")
    if session_id is not None:
        session_storage.delete(session_id)
    logout(request._request)
    return Response({'message': 'Success'})


@swagger_auto_schema(method='post', request_body=ClientCardDetailsSerializer)
@permission_classes([IsAuth])
@api_view(["POST"])
def submit_client_card(request, id):
    try: 
        selected_client_card = PassOrder.objects.get(id=id, status=1) 
    except PassOrder.DoesNotExist: 
        return Response({"message": "Client card not found"}, status=status.HTTP_400_BAD_REQUEST)
    if selected_client_card.name != None and selected_client_card.phone != None:
        selected_client_card.status = 3
        selected_client_card.submited_date = datetime.datetime.now()
        selected_client_card.save()
        serializers = ClientCardDetailsSerializer(selected_client_card)
        
        return Response(serializers.data, status=status.HTTP_200_OK)
    return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=ClientCardSerializer)
@api_view(["POST"])
@permission_classes([IsManagerAuth])
def accept_client_card(request, id):
    user = get_user(request)
    try: 
        selected_client_card = PassOrder.objects.get(id=id, status=3) 
    except PassOrder.DoesNotExist: 
        return Response({"message": "Client card not found"}, status=status.HTTP_400_BAD_REQUEST)
    if selected_client_card.name != None and selected_client_card.phone != None and selected_client_card.submited_date != None:
        selected_client_card.status = 4
        selected_client_card.moderator = user
        selected_client_card.accepted_date = datetime.datetime.now()
        input_string = f"{selected_client_card.name}{selected_client_card.phone}{selected_client_card.created_date}"
        hash_object = hashlib.sha256(input_string.encode())
        hash_base64 = base64.b64encode(hash_object.digest()).decode()
        prefix = hash_base64[:3].upper()
        hash_hex = hash_object.hexdigest()
        hash_int = int(hash_hex, 16)
        suffix = str(hash_int)[:8]
        unique_identifier = f"{prefix}{suffix}"
        selected_client_card.payment_number = unique_identifier
        selected_client_card.save()
        serializers = ClientCardSerializer(selected_client_card)
        return Response(serializers.data, status=status.HTTP_200_OK)
    return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)


class pass_client_card_pass(APIView):
    @swagger_auto_schema(request_body=ClientCardSerializer)
    @method_permission_classes([IsAuth])
    def put(self, request, id):
        try: 
            selected_client_card_pass = PassOrderItems.objects.get(id=id) 
        except PassOrderItems.DoesNotExist: 
            return Response({"message": "Pass not found"}, status=status.HTTP_400_BAD_REQUEST)
        parsed_data = JSONParser().parse(request)
        serializer = ClientCardPassSerializer(selected_client_card_pass, data=parsed_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"message": "Not valid"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @method_permission_classes([IsAuth])
    def delete(self, request, id):
        try: 
            selected_client_card_pass = PassOrderItems.objects.get(id=id) 
        except PassOrderItems.DoesNotExist: 
            return Response({"message": "Pass not found"}, status=status.HTTP_400_BAD_REQUEST)
        selected_client_card_pass.delete()
        return Response({"message": "Deleted succesfuly"}, status=status.HTTP_200_OK)
        
