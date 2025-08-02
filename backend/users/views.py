from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User
from .serializers import UserRegistrationSerializer, UserSerializer
from tenants.models import Tenant


class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint"""
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Create a default tenant for the user with a unique name
            base_name = f"{user.first_name}'s Store"
            tenant_name = base_name
            counter = 1
            
            # Ensure tenant name is unique
            while Tenant.objects.filter(name=tenant_name).exists():
                tenant_name = f"{base_name} ({counter})"
                counter += 1
            
            tenant = Tenant.objects.create(
                name=tenant_name,
                subdomain=f"{user.username.lower().replace('@', '').replace('.', '')}",
                plan_type='free',
                is_active=True,
                owner=user
            )
            
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                'tenant': {
                    'id': tenant.id,
                    'name': tenant.name,
                    'subdomain': tenant.subdomain
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    """Custom login view that returns user data with tokens"""
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Get user data from the request
            user = request.user
            user_data = UserSerializer(user).data
            
            # For now, return empty tenants array since relationship is not established
            response.data.update({
                'user': user_data,
                'tenants': []
            })
        
        return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get current user profile"""
    user = request.user
    tenants = user.tenants.all()
    
    return Response({
        'user': UserSerializer(user).data,
        'tenants': [{
            'id': tenant.id,
            'name': tenant.name,
            'subdomain': tenant.subdomain,
            'is_active': tenant.is_active
        } for tenant in tenants]
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update user profile"""
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'user': serializer.data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 