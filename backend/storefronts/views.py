from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Storefront, Theme, StorefrontSettings
from .serializers import (
    StorefrontSerializer, 
    ThemeSerializer, 
    StorefrontSettingsSerializer,
    CreateStorefrontSerializer
)
from tenants.models import Tenant


class StorefrontListView(generics.ListCreateAPIView):
    """List and create storefronts for the authenticated user"""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateStorefrontSerializer
        return StorefrontSerializer
    
    def get_queryset(self):
        # Get storefronts for user's tenants
        user_tenants = self.request.user.tenants.all()
        return Storefront.objects.filter(tenant__in=user_tenants)
    
    def perform_create(self, serializer):
        # Get the tenant from the request
        tenant_id = self.request.data.get('tenant_id')
        tenant = get_object_or_404(Tenant, id=tenant_id)
        
        # Create storefront with default theme and settings
        storefront = serializer.save(tenant=tenant)
        
        # Create default theme
        theme = Theme.objects.create(
            storefront=storefront,
            name="Default Theme",
            primary_color="#3B82F6",
            secondary_color="#6B7280",
            accent_color="#10B981",
            font_family="Inter",
            is_active=True
        )
        
        # Create default settings
        StorefrontSettings.objects.create(
            storefront=storefront,
            show_product_images=True,
            show_product_prices=True,
            enable_search=True,
            enable_filters=True,
            enable_reviews=True,
            enable_wishlist=True,
            enable_newsletter=True,
            enable_social_sharing=True
        )
        
        return storefront


class StorefrontDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete a storefront"""
    permission_classes = [IsAuthenticated]
    serializer_class = StorefrontSerializer
    
    def get_queryset(self):
        # Get storefronts for user's tenants
        user_tenants = self.request.user.tenants.all()
        return Storefront.objects.filter(tenant__in=user_tenants)


class StorefrontThemeView(generics.RetrieveUpdateAPIView):
    """Manage storefront theme"""
    permission_classes = [IsAuthenticated]
    serializer_class = ThemeSerializer
    
    def get_object(self):
        storefront_id = self.kwargs.get('storefront_id')
        user_tenants = self.request.user.tenants.all()
        storefront = get_object_or_404(
            Storefront, 
            id=storefront_id, 
            tenant__in=user_tenants
        )
        return storefront.theme


class StorefrontSettingsView(generics.RetrieveUpdateAPIView):
    """Manage storefront settings"""
    permission_classes = [IsAuthenticated]
    serializer_class = StorefrontSettingsSerializer
    
    def get_object(self):
        storefront_id = self.kwargs.get('storefront_id')
        user_tenants = self.request.user.tenants.all()
        storefront = get_object_or_404(
            Storefront, 
            id=storefront_id, 
            tenant__in=user_tenants
        )
        return storefront.settings


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def publish_storefront(request, storefront_id):
    """Publish a storefront"""
    user_tenants = request.user.tenants.all()
    storefront = get_object_or_404(
        Storefront, 
        id=storefront_id, 
        tenant__in=user_tenants
    )
    
    storefront.is_published = True
    storefront.save()
    
    return Response({
        'message': 'Storefront published successfully',
        'storefront': StorefrontSerializer(storefront).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unpublish_storefront(request, storefront_id):
    """Unpublish a storefront"""
    user_tenants = request.user.tenants.all()
    storefront = get_object_or_404(
        Storefront, 
        id=storefront_id, 
        tenant__in=user_tenants
    )
    
    storefront.is_published = False
    storefront.save()
    
    return Response({
        'message': 'Storefront unpublished successfully',
        'storefront': StorefrontSerializer(storefront).data
    })


@api_view(['GET'])
def public_storefront(request, subdomain):
    """Public endpoint to view a published storefront"""
    tenant = get_object_or_404(Tenant, subdomain=subdomain, is_active=True)
    storefront = get_object_or_404(
        Storefront, 
        tenant=tenant, 
        is_published=True
    )
    
    return Response({
        'storefront': StorefrontSerializer(storefront).data,
        'theme': ThemeSerializer(storefront.theme).data,
        'settings': StorefrontSettingsSerializer(storefront.settings).data
    }) 