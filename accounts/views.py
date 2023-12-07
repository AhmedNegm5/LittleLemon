from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


                
@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        
        user = None
        
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except ObjectDoesNotExist:
                return Response({'error':'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if not user:
            user = authenticate(username=username, password=password)
            
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token':token.key}, status=status.HTTP_200_OK)

        return Response({'error':'Wrong credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'success':'User logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    if request.method == 'GET':
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    if request.method == 'PUT':
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':'User updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    if request.method == 'DELETE':
        user = request.user
        user.delete()
        return Response({'success':'User deleted'}, status=status.HTTP_200_OK)
    
    return Response({'error':'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

