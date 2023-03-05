from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer, AllUserSerializer, ProfileSerializer
from user.models import Profile

from user.profile import size_compress


@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'user_data': serializer.data})
    else:
        return Response({'error': serializer.errors})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_user(request):
    user = User.objects.filter().exclude(is_staff=True).exclude(username=request.user)
    serializer = AllUserSerializer(user, many=True)
    return Response({'users': serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_user(request):
    user = User.objects.get(username=request.user)
    serializer = AllUserSerializer(user)
    return Response({'user': serializer.data})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    profile_exist = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        if profile_exist:
            serializer = ProfileSerializer(data=request.data, instance=profile_exist)
            if serializer.is_valid():
                serializer.save()
                size_compress(request.user)
                return Response({'user': str(request.user), 'profile_data': serializer.data})
            else:
                return Response({'message': serializer.errors})
        else:
            serializer = ProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                size_compress(request.user)
                return Response({'user': str(request.user), 'profile_data': serializer.data})
            else:
                return Response({'message': serializer.errors})
    if request.method == 'GET':
        serializer = ProfileSerializer(profile_exist)
        return Response({'profile_data': serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    if profile:
        profile.delete()
        message = 'profile deleted successfully.'
    else:
        message = 'profile not exist for this user.'
    return Response({'message': message})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_any_user(request, id):
    user = User.objects.filter(id=id).first()
    if user:
        user.delete()
        message = 'user deleted successfully.'
    else:
        message = 'user not exist.'
    return Response({'message': message})
